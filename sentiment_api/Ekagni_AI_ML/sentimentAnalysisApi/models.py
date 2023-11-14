from django.db import models

# Create your models here.

class TempImage(models.Model):
   image = models.FileField(upload_to="temp/sentiment_analysis/Image/")
   class Meta :
      db_table = "Temporary Images Sentiment Analysis"
      # app_label = 'EKAGNI_AI_ML'

class Monitor(models.Model):
   tag = models.CharField(default=None,max_length=15)
   count = models.IntegerField(default=0)
   class Meta :
      db_table= "New Sentiment Monitoring Table"
