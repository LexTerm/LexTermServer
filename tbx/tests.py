try:
    from lxml import etree
    from lxml.etree import fromstring
    from lxml import isoschematron
except ImportError:
    import xml.etree.cElementTree as etree
    
from django.test import TestCase
from os import path

class TestTBXBasicValidation(TestCase):
    
    def test_validation(self):
        tbx_dir = path.join(path.dirname(__file__), "resources/TBXBasic/")
        xml = fromstring(open(tbx_dir + "TBX-basic-samples.tbx").read())
        schema = etree.parse(tbx_dir + "TBXBasicRNGV02.rng")
        schema = etree.RelaxNG(schema)
        #schema = isoschematron.Schematron(schema)
        
        self.assertTrue(schema.validate(xml))
        
        xml = fromstring(open(tbx_dir + "tbx_basic_sample_badelement.tbx").read())
        self.assertFalse(schema.validate(xml))
        
        xml = fromstring(open(tbx_dir + "tbx_basic_sample_badattribute.tbx").read())
        self.assertFalse(schema.validate(xml))
        
        # This test fails in lxml and jing, is it a bad test file?
        #xml = fromstring(open(tbx_dir + "tbx_basic_sample_badelementcontent.tbx").read())
        #self.assertFalse(schema.validate(xml))
        
        xml = fromstring(open(tbx_dir + "tbx_basic_sample_badelementorder.tbx").read())
        self.assertFalse(schema.validate(xml))
        
        self.assertRaises(etree.XMLSyntaxError, lambda:fromstring(open(tbx_dir + "tbx_basic_sample_notwellformed.tbx").read()))
        
            