from django.contrib import admin
from .models import fitnessPoints, quizUser, runImage

# Register your models here.
admin.site.register(fitnessPoints)
admin.site.register(runImage)
admin.site.register(quizUser)
