from django.contrib import admin

# Register your models here.

from .models import TempImage,Monitor


class MonitorView(admin.ModelAdmin):
   list_display=['tag','count']

admin.site.register(TempImage)
admin.site.register(Monitor,MonitorView)
