from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from Ekagni_AI_ML.settings import *
from .models import TempImage,Monitor
from .forms import *
from .utils import *
import base64
@csrf_exempt
def ping(request):
   return JsonResponse({"status":True})
@csrf_exempt
def sentiment_driver(request):
   try:
      print("sdfjsdk;lfjlskdafj klsd;fjdskfl ",request.FILES.dict())
      print("Dataaaa--->",request.POST.get("option"))
      form = TempImageForm({},{'image' : request.FILES['image0']})
      response = processImageFroAndroid(form,request)
      return response
   except Exception as e:
      try :
         print(request.POST.dict)
         print("Dataaaa--->",request.POST.get("src1"))
         imgdata = base64.b64decode(request.POST.get('src').replace(' ', '+'))
         form = TempImageForm({},{'image':ContentFile(imgdata,"temp.png")})
         response = processImage(form,request)
         return response
      except Exception as e:
         print("file not found in request.post")
   return JsonResponse({
      'error' : "something went wrong"
   })


