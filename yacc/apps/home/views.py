import sys, os
import io
import numpy as np

from PIL import Image
# Make necessary imports
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User

from .models import *
from .forms import ScancardForm

from apps.home.API import api_main
from apps.home.ocr import app_detrec, app_rec, ocr_main, cropper

from mkmsdk.mkm import Mkm
from mkmsdk.api_map import _API_MAP

@login_required(login_url="/login/")
def index(request):
    # Get all cards
    cards = Cartes.objects.prefetch_related('prixhebdo_set').all()

    context = {'segment': 'index', 'cards': cards}

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
    context = {'cards': cards, 'segment': 'collections' }
    html_template = "home/collections.html"
    return render(request, html_template, context)


@login_required(login_url="/login/")
def scancard(request):
    if request.method == 'POST':
        form = ScancardForm(request.POST, request.FILES)
        if form.is_valid():
            print('Carte bien uploadée : Start')
            # traitement
            #Cartes.upload_card(request.FILES['file], request)
            # form.save()
            
            images = request.FILES['file']

            # we need to read the image file
            images = Image.open(io.BytesIO(images.read()))
            # Convert the PIL image to a NumPy array
            np_array_images = np.array(images)
            print("\n\n type \n\n")
            print(type(np_array_images))
            print("\n\n type \n\n") 

            ocr_result = ocr_main.result(np_array_images)
            mkm_sandbox = Mkm(_API_MAP["2.0"]["api"], _API_MAP["2.0"]["api_sandbox_root"])

            for image in ocr_result:
                print(image[0])
                try:
                    data = api_main.card_search(image[0])
                    print("\n\n")
                    for cle, valeur in data.items():
                        print(cle, valeur)
                    tmp_price_guide = data.pop('priceGuide')
                    print("\n\n")
                    for cle, valeur in tmp_price_guide.items():
                        print(cle, valeur)
                    print("\n\n\n\n")

                    print(request.user.id)
                    carte = Cartes()
                    prix = PrixHebdo()
                    auth_user = AuthUser.objects.get(id=request.user.id)

                    carte.num = image[0]
                    carte.nom = data.get('locName', '')
                    carte.image = data.get('image', '')
                    carte.rarity = data.get('rarity', '')
                    carte.category = data.get('categoryName', '')
                    carte.id_user = auth_user
                    carte.save()
                    
                    print("\n \n\n Carte bien enregistrée 1")
                    prix.date_prix = timezone.now()
                    prix.id_cartes = carte
                    prix.sell = tmp_price_guide.get('SELL', '')
                    prix.low = tmp_price_guide.get('LOW', '')
                    prix.trend = tmp_price_guide.get('TREND', '')
                    prix.lowfoil = tmp_price_guide.get('LOWFOIL', '')
                    prix.avg_price = tmp_price_guide.get('AVG', '')
                    prix.lowex = tmp_price_guide.get('LOWEX', '')
                    prix.save()

                    print("\n \n\n Carte bien enregistrée 2")


                    
                except Exception as e:
                    print('failure for image code ' + image[0])
                    print(e)
            
            print('Carte bien uploadée End')
            print(image[0])
    else:
        form = ScancardForm()
    
    context = {'form':form , 'segment': 'scancard'}
    html_template = "home/scancard.html"
    return render(request, html_template, context)

@login_required(login_url="/login/")
def showcard(request,id):
    card = Cartes.objects.get(id=id)
    context = {'card':card,'segment': 'scancard' }
    html_template = "home/showcard.html"
    return render(request, html_template, context)
