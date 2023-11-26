from django.http import HttpResponse

from suspense.futures import get


def django_suspense_loader(request):
    return HttpResponse(get(request.headers.get('SUSPENSE_UID')))
