from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Teams

# Enregistrez le modèle dans l'administration
admin.site.register(Teams)