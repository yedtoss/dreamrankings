from django.contrib import admin

# Register your models here.

from models import Member
import models
admin.site.register(Member)
admin.site.register(models.RatingsPicture)
