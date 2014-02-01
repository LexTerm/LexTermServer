from lex.models import *
from term.models import *
from rest_framework.status import *
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.template.loader import get_template
from django.http import HttpResponse
from django.template.context import Context
import re
from os import path

try:
    from lxml import etree
    from lxml.etree import fromstring
except ImportError:
    import xml.etree.cElementTree as etree

import logging
logger = logging.getLogger(__name__)

TBX_BASIC_PLACEHOLDER = "tbx_basic_term"
WRITTEN_REP_TYPE = "written"


@api_view(('GET',))
def tbx_root(request, format=None):
    return Response({
        'import': reverse('tbx_import', request=request, format=format),
        'export': reverse('tbx_export', request=request, format=format),
        'validate': reverse('tbx_validate', request=request, format=format),
        'url': reverse('tbx', request=request, format=format),
    })


def get_schema():
    tbx_dir = path.join(
        path.dirname(__file__), "resources/TBXBasic/")
    schema = etree.parse(tbx_dir + "TBXBasicRNGV02.rng")
    schema = etree.RelaxNG(schema)
    return schema


class FileSerializer(serializers.Serializer):
    file = serializers.FileField(allow_empty_file=False)


class ValidateView(GenericAPIView):

    """ Upload and XML document for TBX-Basic validation.

        file: the tbx file for validation
     """

    serializer_class = FileSerializer

    def post(self, request):

        if request.FILES.get('file'):
            if not request.FILES['file'].multiple_chunks():
                try:
                    xml = fromstring(request.FILES['file'].read())
                except etree.XMLSyntaxError:
                    return Response(False)
                else:
                    schema = get_schema()
                    return Response(schema.validate(xml))

            else:
                return Response(status=HTTP_400_BAD_REQUEST,
                                data="Uploaded TBX file is too big to process via this interface. ")


class TBXImportView(GenericAPIView):

    """ Upload a TBX file to import """

    serializer_class = FileSerializer

    def post(self, request, format=None):
        serializer = FileSerializer(files=request.FILES)
        if serializer.is_valid():
            logger.debug("Got TBX file, starting import")
            try:
                import_tbx(serializer.object['file'])
            except Exception as e:
                logger.exception("Error importing TBX file")
                return Response("Error importing TBX file: {}".format(e),
                                status=HTTP_400_BAD_REQUEST)
            return Response("Successfully uploaded TBX file", status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        return Response("Upload TBX files here")


class TBXExportView(APIView):

    #TODO export pos
    #TODO export definitions
    def get(self, request, format=None):
        concepts = {}
        for form in Form.objects.filter(is_lemma=True, representations__representation_type__name=WRITTEN_REP_TYPE):
            concept_id = form.lexeme.concept.concept_id
            concepts.setdefault(concept_id, {})
            lang_code = form.lexeme.language.lang_code
            reg_code = form.lexeme.language.region_code
            if reg_code:
                concepts[concept_id].setdefault(lang_code+"-"+reg_code, [])
                concepts[concept_id][lang_code+"-"+reg_code].append(
                    form.representations.get(representation_type__name=WRITTEN_REP_TYPE))
            else:
                concepts[concept_id].setdefault(lang_code, [])
                concepts[concept_id][lang_code].append(
                    form.representations.get(representation_type__name=WRITTEN_REP_TYPE))

        template = get_template('tbx-basic.xml')
        xml = template.render(Context({'concepts': concepts}))
        schema = get_schema()
        if schema.validate(fromstring(xml)):
            return HttpResponse(xml, mimetype="text/xml")
        else:
            return Response(status=HTTP_404_NOT_FOUND,
                            data="Unable to generate valid tbx-basic from current database state.")

XML_NS = "{http://www.w3.org/XML/1998/namespace}"


def import_tbx(tbx_file):
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.parse(tbx_file, parser).getroot()

    # iterate over all term entries and import
    for term_entry in root.iter('termEntry'):
        import_term_entry(term_entry)


def import_term_entry(term_entry):
    concept_id = term_entry.get('id')
    print("importing termEntry: {}".format(concept_id))
    concept = get_or_none(Concept, concept_id=concept_id)
    if not concept:
        # if the concept doesn't already exist, create one
        concept = Concept(concept_id=concept_id)
        concept.save()
        print("created concept: {}".format(concept_id))

    import_definitions(term_entry, concept)
    import_subject_fields(term_entry, concept)

    for lang_set in term_entry.iterchildren('langSet'):
        import_lang_set(lang_set, concept)


def import_definitions(term_entry, concept):
    # print("importing definition for concept: {}".format(concept))
    # get all of several possible descrip elements that has attribute type=definition
    # def_xpath = "(./descrip|./descripGrp/descrip|./langSet/descrip)[@type='definition']"
    def_xpath = ("./descrip[@type='definition']|"
                 "./descripGrp/descrip[@type='definition']|"
                 "./langSet/descrip[@type='definition']")
    # findtext returns the text element of the first match
    # TODO: handle multiple definitions (possibly per-language?)
    definition = term_entry.xpath(def_xpath)
    if definition:
        # add the first definition to the concept
        definition = clean_multiline_text(definition[0].text)
        concept.definition = definition
        concept.save()
        print("imported definition for concept: {}: {}".format(
            concept, definition))


def import_subject_fields(term_entry, concept):
    # TODO: handle subject fields
    pass


def import_lang_set(lang_set, concept):
    code = lang_set.get(XML_NS + 'lang').lower()
    # get rid of locale codes for now (en-gb ==> en)
    code = code.split('-', 1)
    lang_code = code[0]
    reg_code = ''
    if len(code) > 1:
        reg_code = code[1]
    print("importing langSet: {}_{}".format(lang_code, reg_code))
    lang = get_or_none(Language, lang_code=lang_code, region_code=reg_code)
    if not lang:
        # if the language doesn't already exist, create it
        # (use langCode for name, user can change it later)
        lang = Language(lang_code=lang_code, name=lang_code, region_code=reg_code)
        lang.save()
        print("created language: {}".format(lang_code))

    for tig in lang_set.iterchildren('tig'):
        import_term(tig, lang, concept)


def import_term(tig, lang, concept):
    term = tig.findtext('./term')
    print(u"importing term: {}".format(term))
    # TODO: add all termNotes
    pos = tig.findtext("./termNote[@type='partOfSpeech']")
    if not pos:
        logger.warning(
            u"No partOfSpeech data found for {}.".format(term))
        pos = "*"  # Special character for pos
    pos = pos.lower()
    lex_class = get_or_none(LexicalClass, name=pos, language=lang)
    if not lex_class:
        # if the lexical class doesn't already exist, create it
        lex_class = LexicalClass(name=pos, language=lang)
        lex_class.save()
        print("created lexical class: {}".format(pos))
    lexeme = get_or_none(Lexeme, lex_class=lex_class, concept=concept)
    if not lexeme:
        lexeme = Lexeme(language=lang, lex_class=lex_class, concept=concept)
        lexeme.save()
        print(u"created lexeme for term: {}".format(term))
    else:
        # TBX standard (ISO 30042) says that terms are defined as being in lemma / citation form
        # So if we have the lexeme, the term should already exist in the db
        return

    # we can't know what form to create, just use a placeholder until the user changes it
    # first check if the placeholder has already been created
    lemma_form = get_or_none(Form, name=TBX_BASIC_PLACEHOLDER, lexeme=lexeme)
    if not lemma_form:
        lemma_form = Form(
            name=TBX_BASIC_PLACEHOLDER,
            lexeme=lexeme,
            is_lemma=True)
        lemma_form.save()
        print(
            "created temporary form: {} for lexical class: {}".format(TBX_BASIC_PLACEHOLDER, pos))

    rep = Representation(
        name=term,
        form=lemma_form,
        representation_type=RepresentationType.objects.get_or_create(name=WRITTEN_REP_TYPE)[0])
    rep.save()
    print(u"created term: {}".format(term))


# Try to get an object that matches the query. If it doesn't exist, return None
def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def clean_multiline_text(text):
    text = text.translate(None, '\r\n')
    return re.sub(r'\t+', ' ', text)
