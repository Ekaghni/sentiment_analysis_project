from sentimentAnalysisApi.Sentiment_Project.nltk_trial import getSentimentValue,createNewBrand,add_data_to_csv
from . import models,forms
from Ekagni_AI_ML.settings import *
import base64
from .models import TempImage,Monitor
from django.http import JsonResponse, HttpResponse
from threading import Thread
import mimetypes

def evaluatePayload(payload,tempImageObj):
   extension : str = tempImageObj.image.url[tempImageObj.image.url.rindex(".")+1:]
   output_img_path : str =  MEDIA_ROOT+ str(tempImageObj.image.url)[1:]
   noise_level = 3
   scale_ratio : float = 2.0
   color:str = "rgb"
   quality : int = 100
   selected_csv_file: str = "my_reviews.csv"
   option: int = 1
   brandName: str = "Paypal"
   id_value: int = 1
   comments_value: str = "I like the product very much"

   # print("ggggg__>",output_img_path)
   
   

   if("extension" in payload):
      if extension !=  payload['extension'] :
         extension = payload['extension'] 
         output_img_path = output_img_path[0:output_img_path.rindex(".")+1]+extension
   
   
   if("scale_ratio" in payload):
      scale_ratio = payload["scale_ratio"]

   if("noise" in payload):
      scale_ratio = payload["noise"]

   if("noise_level" in payload):
      noise_level = payload["noise_level"]
   
   if("color" in payload):
      color = payload["color"]

   if('quality' in payload):
      quality = payload['quality']
   # print("-----------------END___________________")
   # print("ggggg__>",output_img_path)
   if("selected_csv_file" in payload):
      selected_csv_file = payload["selected_csv_file"]

   if("option" in payload):
      option = payload["option"]

   if("brandName" in payload):
      brandName = payload["brandName"]

   if("id_value" in payload):
      id_value = payload["id_value"]
       
   if("comments_value" in payload):
      comments_value = payload["comments_value"]
   
   return extension,output_img_path,selected_csv_file,option,brandName,id_value,comments_value


def deleteFile(**kwargs):
   print("deleting file")
   while True :
      try :
         if(os.path.exists(kwargs['file'])) :
            os.remove(kwargs['file'])
         return
      except :
         continue
   print("deleted")

def processImageFroAndroid(form,request):
   try :
      # checking validity of the form
      if(form.is_valid()):
         # saving the form if valid 
         tempImageObj = form.save()
         # getting the saved form from database
         tempImageObj = TempImage.objects.get(id=tempImageObj.id)

         # extracting image file url
         file = (MEDIA_ROOT+str(tempImageObj.image.url)[1:])

         # evaluating payload
         extension,output_img_path,selected_csv_file,option,brandName,id_value,comments_value=evaluatePayload(request.POST.dict(),tempImageObj)

         print("OUtput path : ",output_img_path)
         option = int(option)

         if option==1:
            print("Going to option 1")
            sentiment_val = getSentimentValue(selected_csv_file)
            return JsonResponse({
                'Sentiment Value' : sentiment_val
            })
         elif option==2:
            createNewBrand(brandName)
            return JsonResponse({
                'Brand Result' : "Brand created successfully"
            })
         elif option==3:
            id_value = int(id_value)
            comments_value = str(comments_value)
            add_data_to_csv(selected_csv_file,id_value,comments_value)
            return JsonResponse({
                'Comment addition result' : "Data added successfully"
            })
         else:
            return JsonResponse({
                'Error' : "Sorry"
            })
         

         

         path = open(output_img_path, 'rb')
         # getting type of file for html headers
         mime_type, _ = mimetypes.guess_type(file)

      
         #print(my_string)
         # deleting the saved model to free up space after operations in a different thread so that the response is send quickly
         if(file != output_img_path) :
            Thread(target=deleteFile,kwargs={"file":output_img_path}).start()
         Thread(target=tempImageObj.delete).start()
         # sending the response
         return HttpResponse(path,content_type=mime_type)
      else :
         # printing the form if it is not valid for debugging
         print(form)
         pass
   except Exception as e:
      print("Except 1")
      # printing exception that may occur for debugging 
      print(e)
      

def processImage(form,request):
   try :
      # checking validity of the form
      if(form.is_valid()):
         # saving the form if valid 
         tempImageObj = form.save()
         # getting the saved form from database
         tempImageObj = TempImage.objects.get(id=tempImageObj.id)
         # extracting image file url
         file = (MEDIA_ROOT+str(tempImageObj.image.url)[1:])
         # evaluating payload
         extension,output_img_path,noise_level,color,scale_ratio,quality=evaluatePayload(request.POST.dict(),tempImageObj)

         print("OUtput path : ",output_img_path)
         
         # making a anime
         operateImage(
            input_img_path = file,
            output_img_path = output_img_path,
            extension = extension,
            scale_ratio = scale_ratio,
            noise_level = noise_level,
            
            )

         # getting file from the url
         path = open(output_img_path, 'rb')
         # getting type of file for html headers
         mime_type, _ = mimetypes.guess_type(file)

         with open(output_img_path, "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
         #print(my_string)
         # deleting the saved model to free up space after operations in a different thread so that the response is send quickly
         if(file != output_img_path) :
            Thread(target=deleteFile,kwargs={"file":output_img_path}).start()
         Thread(target=tempImageObj.delete).start()
         # sending the response
         return HttpResponse(my_string,content_type=mime_type)
      else :
         # printing the form if it is not valid for debugging
         print(form)
         pass
   except Exception as e:
      print("Except 1")
      
      # printing exception that may occur for debugging 
      print(e)

def increaseRequestcount():
   print("Increamenting current count ")
   current = Monitor.objects.get(tag="Current")
   current.count = current.count + 1
   current.save()
   print("Increamenting current count done ...")


def decreaseRequestcount():
   print("Decreamenting current count ")
   current = Monitor.objects.get(tag="Current")
   total = Monitor.objects.get(tag="Total")
   total.count = total.count + 1
   current.count = current.count - 1
   current.save()
   total.save()
   print("Decreamenting current count done ... ")
