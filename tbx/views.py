from lex.models import *
from term.models import *
from rest_framework.status import *
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.template.loader import get_template
from django.http import HttpResponse
from django.template.context import Context
from django.utils.encoding import smart_text
import re
from os import path

try:
    from lxml import etree
    from lxml.etree import fromstring, tostring
except ImportError:
    import xml.etree.cElementTree as etree

import logging
logger = logging.getLogger(__name__)


@api_view(('GET',))
def tbx_root(request, format=None):
    return Response({
        '_links': {
            'import': reverse('tbx_import', request=request, format=format),
            'export': reverse('tbx_export', request=request, format=format),
            'validate': reverse('tbx_validate', request=request, format=format),
            'self': reverse('tbx', request=request, format=format)
        }
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
        for lex_form in LexicalForm.objects.all():
            concept_id = lex_form.lexeme.concept.concept_id
            concepts.setdefault(concept_id, {})
            lang_code = lex_form.lexeme.language.langCode
            concepts[concept_id].setdefault(lang_code, [])
            concepts[concept_id][lang_code].append(lex_form)

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
    lang_code = lang_set.get(XML_NS + 'lang').lower()
    # get rid of locale codes for now (en-gb ==> en)
    lang_code = lang_code.split('-', 1)[0]
    print("importing langSet: {}".format(lang_code))
    lang = get_or_none(Language, langCode=lang_code)
    if not lang:
        # if the language doesn't already exist, create it
        # (use langCode for name, user can change it later)
        lang = Language(langCode=lang_code, name=lang_code)
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
            u"Could not import term '{}': no partOfSpeech data found".format(term))
        return
    pos = pos.lower()
    lex_class = get_or_none(LexicalClass, name=pos, language=lang)
    if not lex_class:
        # if the lexical class doesn't already exist, create it
        lex_class = LexicalClass(name=pos, language=lang)
        lex_class.save()
        print("created lexical class: {}".format(pos))
    # TBX standard (ISO 30042) says that terms are defined as being in lemma / citation form
    # So we just grab the form with preference=1, because we don't have enough information
    # to intelligently fall back to a different form
    lemma_form = get_or_none(Form, lexicalClass=lex_class, preference=1)
    if not lemma_form:
        # we can't know what form to create, just use a placeholder until the user changes it
        # first check if the placeholder has already been created
        lemma_form = get_or_none(Form, name='term', lexicalClass=lex_class)
        if not lemma_form:
            lemma_form = Form(
                name='term', lexicalClass=lex_class, preference=1000)
            lemma_form.save()
            print(
                "created temporary form: term for lexical class: {}".format(pos))
    # make an attempt to check if the lexeme already exists (based on its
    # lemma)
    lexeme = get_or_none(Lexeme, language=lang,
                         lexicalClass=lex_class, lemma=term)
    if not lexeme:
        lexeme = Lexeme(language=lang, lexicalClass=lex_class, concept=concept)
        lexeme.save()
        print(u"created lexeme for term: {}".format(term))
    else:
        # the term already exists, we're done
        # set the concept in case it wasn't already
        print(u"term: {} already exists".format(term))
        lexeme.concept = concept
        lexeme.save()
        return
    lex_term = LexicalForm(lexeme=lexeme, form=lemma_form, representation=term)
    lex_term.save()
    print(u"created term: {}".format(term))


# Try to get an object that matches the query. If it doesn't exist, return None
def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

#TODO: Blocks of text in the XML have newlines and tabs for alignment - clean
# these up


def clean_multiline_text(text):
    text = text.translate(None, '\r\n')
    return re.sub(r'\t+', ' ', text)
