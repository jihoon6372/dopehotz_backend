from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'api', settings.ROOT_URLCONF, name='api'),
    host(r'adm', settings.ADMIN_URLCONF, name='admin'),
    host(r'auth', settings.AUTH_URLCONF, name='auth'),
    host(r'tower', settings.TOWER_URLCONT, name='tower'),

    host(r'test.api', settings.ROOT_URLCONF, name='test-api'),
    host(r'test.adm', settings.ADMIN_URLCONF, name='test-admin'),
    host(r'test.auth', settings.AUTH_URLCONF, name='test-auth'),
    host(r'test.tower', settings.TOWER_URLCONT, name='test-tower'),

    host(r'local.api', settings.ROOT_URLCONF, name='local-api'),
    host(r'local.adm', settings.ADMIN_URLCONF, name='local-admin'),
    host(r'local.auth', settings.AUTH_URLCONF, name='local-auth'),
    host(r'local.tower', settings.TOWER_URLCONT, name='local-tower'),
)