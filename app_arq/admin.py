from django.contrib import admin
from .models import Proyecto, Trabajador, User
from datetime import datetime

# Register your models here.
admin.site.register(Proyecto)
admin.site.register(Trabajador)