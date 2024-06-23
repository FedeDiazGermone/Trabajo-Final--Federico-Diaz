from django.contrib import admin

# Register your models here.
from django.contrib import admin
from datetime import datetime
from .models import *

class ProdAdmin(admin.ModelAdmin):
  list_display = ['nombre', 'marca', 'precio_costo', 'tipo']
  search_fields = ['nombre', 'marca']
  list_filter = ['nombre']

class CompraAdmin(admin.ModelAdmin):
  list_display = ["nro","fecha_compra", "cantidad","precio_venta","antiguedad"]

  def antiguedad(self, object):
    if object.fecha_compra:
      return (datetime.now().date() - object.fecha_compra).days

# Register your models here.
admin.site.register(Producto, ProdAdmin)
admin.site.register(Proveedor)
admin.site.register(Compra, CompraAdmin)
admin.site.register(Avatar)

