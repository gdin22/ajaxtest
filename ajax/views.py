from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from ajax.models import Contacts
import json
from pymongo import MongoClient
conn = MongoClient('localhost', 27017)
asinDict = conn.amazon.asin.find_one()['asinToSku']


@csrf_exempt
def ajax_submit(request):
    if request.method == 'POST':
        print(request.POST)
        return HttpResponse("home")
    return render(request, 'sub.html')


@csrf_exempt
def demo_ajax(request):
    return render(request, 'demo_ajax.html')


@csrf_exempt
def demo_add(request):
    a = request.GET['a']
    b = request.GET['b']

    if request.is_ajax():
        ajax_string = 'ajax request'
    else:
        ajax_string = 'not ajax request'

    c = int(a) + int(b)
    r = HttpResponse(ajax_string + str(c))
    return r


@csrf_exempt
def get_number(request):
    print(request.GET)
    r = HttpResponse('<option value="100">100</option> <option value="200">200</value>')
    return r


@csrf_exempt
def get_cloud(request):
    if request.method == 'POST':
        asinDict = conn.amazon.asin.find_one()['asinToSku']
        asinList = list(asinDict)
        q = request.POST['q']
        if q not in asinList:
            rejson = []
            for asin in asinList:
                rejson.append(inThisAsin(q, asin))
            return HttpResponse(json.dumps(rejson), content_type='application/json')
        else:
            size = request.POST['size']
    return render(request, 'cloud.html')


def inThisAsin(word, asin):
    if word in asin:
        return asin
    else:
        return '0'
