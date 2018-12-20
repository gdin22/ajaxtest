from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ajax.makewordcloud import makeWordCloud
from pymongo import MongoClient
conn = MongoClient('localhost', 27017)


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
        comment = conn.amazon.comment
        q = request.POST['q']
        if q not in asinList:
            rejson = []
            for asin in asinList:
                rejson.append(inThisAsin(q, asin))
            return HttpResponse(json.dumps(rejson), content_type='application/json')
        else:
            print(q)
            masin = asinDict[q]
            print(masin)
            colors = [com['color'] for com in comment.find({'asin': masin})]
            colors = list(set(colors))
            sizes = [com['size'] for com in comment.find({'asin': masin})]
            sizes = list(set(sizes))
            stars = [com['star'] for com in comment.find({'asin': masin})]
            stars = list(set(stars))
            try:
                colors.remove('')
            except:
                pass
            try:
                sizes.remove('')
            except:
                pass
            try:
                stars.remove('')
            except:
                pass
            alllist = ['real']
            colorhtml = gen_html(colors)
            alllist.append(colorhtml)
            sizehtml = gen_html(sizes)
            alllist.append(sizehtml)
            starhtml = gen_html(stars)
            alllist.append(starhtml)
            print(alllist)
            return HttpResponse(json.dumps(alllist), content_type='application/json')
    return render(request, 'cloud.html')


def inThisAsin(word, asin):
    if word in asin:
        return asin
    else:
        return '0'


# 这个函数生成select 代码
def gen_html(list):
    html = []
    for i in list:
        html.append('<option value = "%s"> %s </ option>' % (i, i))
    html = ' '.join(html)
    return html


@csrf_exempt
def make_image(request):
    searchDict = {}
    if request.method == 'POST':
        asinDict = conn.amazon.asin.find_one()['asinToSku']
        asin = request.POST['asin']
        masin = asinDict[asin]
        color = request.POST['color']
        size = request.POST['size']
        star = request.POST['star']
        print(request.POST)
        searchDict['asin'] = masin
        if color != 'all':
            searchDict['color'] = color
        if size != 'all':
            searchDict['size'] = size
        if star != 'all':
            searchDict['star'] = float(star)

        print(searchDict)
        make = makeWordCloud()
        make.getcloud(searchDict)
        return render(request, 'demo_ajax.html')
