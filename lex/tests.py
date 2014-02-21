from django.test import TestCase
from lex.models import Language, LexicalClass, Lexeme, Form,\
    Feature, FeatureValue
from term.models import Concept


class UniqueFeatureConstraintTest(TestCase):
    """
    Tests for assuring that a particular Form does not have
    multiple values from the same Feature.
    """

    def test_uniqueness_algorithm(self):
        number = Feature.objects.create(name="NUMBER")
        gender = Feature.objects.create(name="GENDER")
        case = Feature.objects.create(name="CASE")

        sing = FeatureValue.objects.create(feature=number, name="sing")
        #plural = FeatureValue.objects.create(feature=number, name="plural")

        m = FeatureValue.objects.create(feature=gender, name="m")
        f = FeatureValue.objects.create(feature=gender, name="f")
        #n = FeatureValue.objects.create(feature=gender, name="n")

        nom = FeatureValue.objects.create(feature=case, name="nom")
        #gen = FeatureValue.objects.create(feature=case, name="gen")
        #acc = FeatureValue.objects.create(feature=case, name="acc")
        #dat = FeatureValue.objects.create(feature=case, name="dat")
        #abl = FeatureValue.objects.create(feature=case, name="abl")

        lang = Language.objects.create(lang_code="la", name="latintest")
        pos = LexicalClass.objects.create(language=lang, name="postest")
        conc = Concept.objects.create()
        lex = Lexeme.objects.create(lexical_class=pos, concept=conc)

        terra = Form.objects.create(lexeme=lex, name="nom fem sing")
        terra.features.add(nom)
        terra.features.add(sing)

        self.assertNotIn(
            f.feature,
            Feature.objects.filter(values__forms=terra))
        terra.features.add(f)
        self.assertIn(f.feature, Feature.objects.filter(values__forms=terra))
        self.assertEqual(
            len(terra.features.all()),
            len(Feature.objects.filter(values__forms=terra).distinct()))
        terra.features.add(m)
        self.assertEqual(
            len(terra.features.all()),
            len(Feature.objects.filter(values__forms=terra).distinct()))
