from rest_framework.views import APIView
from rest_framework.request import Request
from os import path
from rest_framework.response import Response
from django.forms.forms import Form
from django import forms
import rest_framework
from pkg_resources import ResourceManager
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.serializers import Serializer
from rest_framework import serializers

try:
    from lxml import etree
    from lxml.etree import fromstring
except ImportError:
    import xml.etree.cElementTree as etree

class SimpleFileSerializer(Serializer):
    
    file = serializers.FileField()
    
    
CreateAPIView
class ValidateView(GenericAPIView):
    """ Upload and XML document for TBX-Basic validation.
    
        file: the tbx file for validation
     """
    
    serializer_class = SimpleFileSerializer
    
    def post(self, request):
        
        if request.FILES.get('file'):
            if not request.FILES['file'].multiple_chunks():
                try:
                    xml = fromstring(request.FILES['file'].read())
                except etree.XMLSyntaxError:
                    return Response(False)
                else:
                    tbx_dir = path.join(path.dirname(__file__), "resources/TBXBasic/")
                    schema = etree.parse(tbx_dir + "TBXBasicRNGV02.rng")
                    schema = etree.RelaxNG(schema)
                    
                    return Response(schema.validate(xml))

            else:
                raise ErrorResponse(status.HTTP_400_BAD_REQUEST, "Uploaded TBX file is too big to process via this interface. ")
    