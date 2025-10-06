class CrossOriginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Add COOP and COEP headers to the response
        response['Cross-Origin-Opener-Policy'] = 'unsafe-none'  # Only allows interaction with the same origin
        response['Cross-Origin-Embedder-Policy'] = 'require-corp'  # Requires the cross-origin content to explicitly allow embedding

        return response
