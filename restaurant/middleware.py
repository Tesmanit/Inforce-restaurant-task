class AppVersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.app_version = request.headers.get("X-App-Version")
        return self.get_response(request)
