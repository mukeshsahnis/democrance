from django.conf import settings
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.http import url_has_allowed_host_and_scheme


def get_next_page(next_value, default):
    next_page = next_value or default
    if next_page and not "/" in next_page:
        try:
            reverse(next_page)
        except NoReverseMatch:
            next_page = default
    if not url_has_allowed_host_and_scheme(
        next_page,
        allowed_hosts=settings.ALLOWED_HOSTS,
    ):
        next_page = default
    return next_page
