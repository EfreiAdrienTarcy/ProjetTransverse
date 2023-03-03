from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect

from .models import *

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def collections_index(request):
    # Get all cards
    cards = Cartes.objects.all()
    context = {'cards': cards }
    html_template = "home/collections.html"
    return render(request, html_template, context)


@login_required(login_url="/login/")
def scancard(request):
    context = { }
    html_template = "home/scancard.html"
    return render(request, html_template, context)

@login_required(login_url="/login/")
def showcard(request,id):
    card = Cartes.objects.get(id=id)
    context = {'card':card}
    html_template = "home/showcard.html"
    return render(request, html_template, context)