import re
import platform
from ipware.ip import get_real_ip
from django.conf import settings
from django.http import JsonResponse


class AccessRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def is_trusted_ip(val, trusted_proxies=settings.IPWARE_TRUSTED_PROXY_LIST):
        ips = [ip.strip().lower() for ip in val.split(',')]
        for proxy in trusted_proxies:
            if proxy in ips[-1]:
                return True
        return False

    def process_view(self, request, _, __, ___):
        if 'local' in platform.node():
            return

        if settings.IP_LIMIT is True:
            if self.is_trusted_ip(get_real_ip(request)) is True:
                return
        else:
            return

        return JsonResponse({
            'exception': 'Forbidden'
        }, status=403)
