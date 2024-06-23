from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Producto(models.Model):

  codigo = models.CharField(max_length=30)
  nombre = models.CharField(max_length=30)
  marca = models.CharField(max_length=30)  
  precio_costo = models.FloatField()  
  tipo = models.CharField(max_length=30)

  class Meta():

    verbose_name = 'Product'
    verbose_name_plural = 'The producto'
    ordering = ('nombre', 'marca')
    unique_together = ('nombre', 'marca')

  def __str__(self):    
    return f'{self.nombre} - {self.marca} - {self.precio_costo} - {self.tipo }'

class Proveedor(models.Model):

  codigo = models.CharField(max_length=30)
  nombre = models.CharField(max_length=30)  
  email = models.EmailField()
  telefono = models.CharField(max_length=30)    
  productos = models.ManyToManyField(Producto)
  ##productos = models.ManyToManyField(Producto, through='Compra')

  def __str__(self):    
    return f'{self.codigo} - {self.nombre} - {self.email} - {self.telefono}'
  

class Compra(models.Model):

  nro = models.IntegerField()
  fecha_compra = models.DateField()  
  cantidad = models.IntegerField()  
  precio_venta = models.FloatField()
  producto = models.ForeignKey(Producto, on_delete=models.CASCADE,null=True)    
  proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE,null=True)      

  def __str__(self):    
    return f'{self.nro} - {self.fecha_compra} - {self.cantidad}'

  
  
class Avatar(models.Model):

  user = models.OneToOneField(User, on_delete=models.CASCADE)
  imagen = models.ImageField(upload_to='avatares', blank=True, null=True)
