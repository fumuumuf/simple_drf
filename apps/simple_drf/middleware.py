import threading

THREAD_LOCAL = threading.local()

DB_MAP = {
    'thor': 'thor',
    'potter': 'potter'
}


def get_current_db_name():
    return getattr(THREAD_LOCAL, "DB", None)


def set_db_for_router(db):
    setattr(THREAD_LOCAL, "DB", db)


def _hostname_from_request(request):
    # split on `:` to remove port
    return request.get_host().split(':')[0].lower()


def _tenant_db_from_request(request):
    hostname = _hostname_from_request(request)
    subdomain_prefix = hostname.split('.')[0]
    return DB_MAP.get(subdomain_prefix)


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        db = _tenant_db_from_request(request)
        set_db_for_router(db)
        response = self.get_response(request)
        return response
