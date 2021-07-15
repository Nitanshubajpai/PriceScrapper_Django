from django.http import request
from django.shortcuts import render
import json
# Create your views here.

def index(request):
    data = open('scrapper/static/amazon/price.jsonl').read()
    jsonData = json.loads(data)
    jsondata1 = json.dumps(jsonData)
    return render(request, "scrapper/index.html", context = {'price' : jsondata1})