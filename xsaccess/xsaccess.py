from django import http

try:
    import settings
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

class XsAccessMiddleware(object):
    def process_request(self, request):
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)
            return response
        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response
        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS
        response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)
        return response