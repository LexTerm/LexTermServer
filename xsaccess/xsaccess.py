from django import http

class XsAccessMiddleware(object):
    def process_request(self, request):
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = "*"
            response['Access-Control-Allow-Methods'] = "OPTIONS,POST,GET,PUT,DELETE,HEAD"
            if request.method == "OPTIONS":
                response['Access-Control-Allow-Headers'] = request.META['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']
            return response
        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response
        response['Access-Control-Allow-Origin']  = "*"
        response['Access-Control-Allow-Methods'] = "OPTIONS,POST,GET,PUT,DELETE,HEAD"
        return response
