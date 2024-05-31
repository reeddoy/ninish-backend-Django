from django.contrib import admin
from .models import Quiz, Option, ConductingTime, Category

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Option)
admin.site.register(Category)
admin.site.register(ConductingTime)