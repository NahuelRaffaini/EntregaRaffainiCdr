from django.contrib import admin
from .models import Proyecto, Trabajador, Material
# Register your models here.
admin.site.register(Proyecto)
admin.site.register(Trabajador)
admin.site.register(Material)