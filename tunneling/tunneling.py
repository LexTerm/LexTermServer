class TunnelingMiddleware(object):
    def process_request(self, request):
        if request.META.has_key('HTTP_X_METHODOVERRIDE'):
            http_method = request.META['HTTP_X_METHODOVERRIDE'].upper()
            request.method = http_method
            request.META['REQUEST_METHOD'] = http_method
        return None