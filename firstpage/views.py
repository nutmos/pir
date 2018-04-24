from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import json

from firstpage.models import *

# Create your views here.

def firstpage(request):
    template = loader.get_template('firstpage.html')
    return HttpResponse(template.render({}, request))

def non_pir(request):
    template = loader.get_template('non-pir.html')
    return HttpResponse(template.render({}, request))

def get_ticker(request):
    ticker_raw = Stock.objects.raw("SELECT id, ticker FROM Stock_Price")
    ticker = [s.ticker for s in ticker_raw]
    return HttpResponse(json.dumps(ticker), content_type="application/json")
