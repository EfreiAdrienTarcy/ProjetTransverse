import sys, os
# Get working directory and add ocr and API to it
sys.path.append(os.path.join(os.getcwd(),'ocr'))
sys.path.append(os.path.join(os.getcwd(),'API'))
sys.path.append(".")

# Make necessary imports
from ocr import app_detrec, app_rec, ocr_main, cropper
from API import api_main
from mkmsdk.mkm import Mkm
from mkmsdk.api_map import _API_MAP

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect

from .models import *
from .forms import ScancardForm

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
    if request.method == 'POST':
        form = ScancardForm(request.POST, request.FILES)
        if form.is_valid():
            # traitement
            #Cartes.upload_card(request.FILES['file], request)
            # form.save()
            images = request.FILES['file']

            detandrec,reconly=app_detrec.detrec(images),app_rec.rec(images)

            ocr_result = ocr_main.result(images)

            mkm_sandbox = Mkm(_API_MAP["2.0"]["api"], _API_MAP["2.0"]["api_sandbox_root"])

            for image in ocr_result:
                print(image[0])
                try:
                    api_main.card_search(image[0])
                except:

                    print('failure for image code' + image[0])

            print('Carte bien uploadée')
    else:
        form = ScancardForm()
    
    context = {'form':form }
    html_template = "home/scancard.html"
    return render(request, html_template, context)

@login_required(login_url="/login/")
def showcard(request,id):
    card = Cartes.objects.get(id=id)
    context = {'card':card}
    html_template = "home/showcard.html"
    return render(request, html_template, context)
