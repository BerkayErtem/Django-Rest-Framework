from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
def crypto(request):
    url = "https://api.nomics.com/v1/currencies/sparkline?key=ba959039ee63e8de30b509c1df7e29f5b2975301&ids=BTC&start=2021-04-14T00%3A00%3A00Z"
    response=(requests.get(url))
    #return HttpResponse(response.status_code)
    return JsonResponse(response.json(), safe=False)
