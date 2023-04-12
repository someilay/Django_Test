from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template import loader
from . import models

from typing import List, Dict


def index(request: WSGIRequest) -> HttpResponse:
    menus: List[models.Menu] = [menu for menu in models.Menu.objects.all()]
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'menus': menus}, request))


def menu_view(request: WSGIRequest, menu_id: int) -> HttpResponse:
    template = loader.get_template('menu_example.html')
    return HttpResponse(template.render({'menu_id': menu_id, 'chosen_id': None}, request))


def entry_view(request: WSGIRequest, menu_id: int, entry_id: int) -> HttpResponse:
    try:
        template = loader.get_template('menu_example.html')
        return HttpResponse(template.render({'menu_id': menu_id, 'chosen_id': entry_id}, request))
    except ObjectDoesNotExist:
        return HttpResponseNotFound('No such menu!')
