from django import http

try:
    import settings
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

def setHeaders(req, resp):
	resp['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS
	if req.method === "OPTIONS":
		resp['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)
		if 'HTTP_ACCESS_CONTROL_REQUEST_HEADERS' in req.META:
			resp['Access-Control-Allow-Headers'] = req.META['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']
				
class XsAccessMiddleware(object):
    def process_request(self, request):
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            setHeaders(request, response)
            return response
        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response
        setHeaders(request, response)
        return response