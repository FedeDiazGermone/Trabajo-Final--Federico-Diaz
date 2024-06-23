from django.shortcuts import render
from django.http import HttpResponse

from .models import Producto, Proveedor, Compra, Producto, Avatar
##from .forms import ProdFormulario, ProvFormulario, CompraFormulario,CustomUserCreationForm, UserEditForm, AvatarFormulario
from .forms import *

from django.urls import reverse_lazy

from typing import Any
from django.db.models.query import QuerySet

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect




TEMPLATE_INICIO = "inicio.html"

## https://github.com/MauriiAC/CoderProjects54145/blob/main/AppCoder/views.py

# Create your views here.

def inicio(req):

  try:
    avatar = Avatar.objects.get(user=req.user.id)
    return render(req, "inicio.html", {"url": avatar.imagen.url})  
  except Exception:
    return render(req, TEMPLATE_INICIO)
  

def about(request):
    return render(request, 'about.html')


def producto(codigo, nombre, marca, precio_costo, tipo):

  nuevo_producto = Producto(codigo=codigo, nombre = nombre, marca = marca, precio_costo = precio_costo, tipo = tipo)
  nuevo_producto.save()

  return HttpResponse(f"""
    <p>Producto: {nuevo_producto.nombre} - Marca: {nuevo_producto.marca} creado!</p>
""")


def producto_formulario(req):
  
  if req.method == 'POST':

    formulario = ProdFormulario(req.POST)

    if formulario.is_valid():

        data = formulario.cleaned_data

        nuevo_prod = Producto(codigo=data['codigo'], nombre=data['nombre'], marca=data['marca'], precio_costo=data['precio_costo'], tipo=data['tipo'])
        nuevo_prod.save()

        return render(req, TEMPLATE_INICIO, {"message": "Producto creado con éxito"})
    
    else:

        return render(req, TEMPLATE_INICIO, {"message": "Datos no válidos"})
  
  else:

    formulario = ProdFormulario()

    return render(req, "prod_formulario.html", {"formulario": formulario})


def productos(req, page=0):

  cant_por_pagina = 3
  total_productos = Producto.objects.count()
  max_page = (total_productos - 1) // cant_por_pagina  


  if req.GET.get('direccion') == 'next' and page < max_page:
    page += 1
  elif req.GET.get('direccion') == 'previous' and page > 0:  
    page -= 1

  
  inicio = int(page) * cant_por_pagina
  final = (int(page)+1) * cant_por_pagina
  
  lista = Producto.objects.all()[inicio:final]

  return render(req, "productos.html", {"lista_productos": lista, "current_page": page, "max_page": max_page})



def lista_productos(req):

  productos = Producto.objects.all()

  return render(req, "leer_productos.html", {"productos": productos})



def proveedores(req, page=0):

  cant_por_pagina = 3
  total_productos = Producto.objects.count()
  max_page = (total_productos - 1) // cant_por_pagina  


  if req.GET.get('direccion') == 'next' and page < max_page:
    page += 1
  elif req.GET.get('direccion') == 'previous' and page > 0:  
    page -= 1

  
  inicio = int(page) * cant_por_pagina
  final = (int(page)+1) * cant_por_pagina
  
  lista = Proveedor.objects.all()[inicio:final]

  return render(req, "proveedores.html", {"lista_proveedores": lista, "current_page": page, "max_page": max_page})

  


def crear_producto(req):

  if req.method == 'POST':

    formulario = ProdFormulario(req.POST)

    if formulario.is_valid():

        data = formulario.cleaned_data

        nuevo_prod = Producto(codigo=data['codigo'], nombre=data['nombre'], marca=data['marca'], precio_costo=data['precio_costo'], tipo=data['tipo'])
        nuevo_prod.save()

        return render(req, TEMPLATE_INICIO, {"message": "Producto creado con éxito"})
    
    else:

        return render(req, TEMPLATE_INICIO, {"message": "Datos no válidos"})
  
  else:

    formulario = ProdFormulario(req.POST)

    return render(req, "prod_formulario.html", {"formulario": formulario  })
  
  
def eliminar_producto(req, codigo):

  if req.method == 'POST':

    profesor = Producto.objects.get(codigo=codigo)
    profesor.delete()

    productos = Producto.objects.all()

  return render(req, "leer_productos.html", {"productos": productos})


def editar_producto(req, codigo):

  if req.method == 'POST':

    formulario = ProdFormulario(req.POST)

    if formulario.is_valid():

      data = formulario.cleaned_data
      producto = Producto.objects.get(codigo=codigo)

      producto.nombre = data["nombre"]
      producto.marca = data["marca"]
      producto.precio_costo = data["precio_costo"]
      producto.tipo = data["tipo"]

      producto.save()

      return render(req, TEMPLATE_INICIO, {"message": "Producto actualizado con éxito"})
    
    else:

      return render(req, TEMPLATE_INICIO, {"message": "Datos no válidos"})
  
  else:

    producto = Producto.objects.get(codigo=codigo)

    formulario = ProdFormulario(initial={
      "nombre": producto.nombre,
      "marca": producto.marca,
      "precio_costo": producto.precio_costo,
      "tipo": producto.tipo,
    })

    return render(req, "editar_producto.html", {"formulario": formulario, "codigo": producto.codigo})
  

def busqueda_marca(req):

    return render(req, "busqueda_marca.html", {})


def buscar(req):

  marca = req.GET.get("marca")  
  if marca:
    ### marca = req.GET["marca"]

    productos = Producto.objects.filter(marca__icontains=marca)

    return render(req, "resultadoBusqueda.html", {"productos": productos, "marca": marca})
  else:      
      return render(req, TEMPLATE_INICIO, {"message": "No envias el dato de la marca"})


#### Proveedor

def proveedor(codigo, nombre, email, telefono):

  nuevo_prov = Proveedor(nombre=nombre, codigo=codigo, email=email, telefono=telefono)
  nuevo_prov.save()

  return HttpResponse(f"""
    <p>Código: {nuevo_prov.codigo} - Nombre: {nuevo_prov.nombre} creado!</p>
  """)


@login_required
def proveedor_formulario(req):
    if req.method == 'POST':
        formulario = ProvFormulario(req.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data

            nuevo_prov = Proveedor(
                codigo=data['codigo'],
                nombre=data['nombre'],
                email=data['email'],
                telefono=data['telefono'],
            )
            nuevo_prov.save()

            return render(req, "inicio.html", {"message": "Proveedor creado con éxito"})
        else:
            return render(req, "proveedor_formulario.html", {"formulario": formulario})

    else:
        formulario = ProvFormulario()
        return render(req, "proveedor_formulario.html", {"formulario": formulario})
        

def lista_proveedores(req):

  try:

    if req.user.proveedor:
      
      proveedores = Proveedor.objects.all()

      return render(req, "leer_proveedores.html", {"proveedores": proveedores})
    
    else:

      return HttpResponseRedirect('/comp-app/')

  except Exception:

      return HttpResponseRedirect('/comp-app/')


def crea_proveedor(req):

  if req.method == 'POST':

    info = req.POST

    formulario = ProvFormulario({
      "codigo": info["codigo"],
      "nombre": info["nombre"],
      "telefono": info["telefono"],
      "email": info["email"],      
    })

    user_form = UserCreationForm({
      "username": info["username"],
      "password1": info["password1"],
      "password2": info["password2"],
    })

    if formulario.is_valid() and user_form.is_valid():

      data = formulario.cleaned_data

      data.update(user_form.cleaned_data)

      user = User(username=data["username"])
      user.set_password(data["password1"])
      user.save()

      nuevo_proveedor = Proveedor(codigo=data['codigo'], nombre=data['nombre'], telefono = data['telefono'],email=data['email'], user_id=user)      
      nuevo_proveedor.save()

      return render(req, "inicio.html", {"message": "Proveedor creado con éxito"})
    
    else:

      return render(req, "inicio.html", {"message": "Datos inválidos"})
  
  else:

    formulario = ProvFormulario()
    user_form = UserCreationForm()
    

    return render(req, "proveedor_formulario.html", {"formulario": formulario, "userForm": user_form})
  

def eliminar_proveedor(req, id):

  if req.method == 'POST':

    proveedor = Proveedor.objects.get(id=id)
    proveedor.delete()

    proveedores = Proveedor.objects.all()

  return render(req, "leer_proveedor.html", {"proveedores": proveedores })


def editar_proveedor(req, id):

  if req.method == 'POST':

    formulario = ProvFormulario(req.POST)

    if formulario.is_valid():

      data = formulario.cleaned_data
      proveedor = Proveedor.objects.get(id=id)

      proveedor.codigo = data["codigo"]
      proveedor.nombre = data["nombre"]
      proveedor.email = data["email"]
      proveedor.telefono = data["telefono"]      

      proveedor.save()

      return render(req, "inicio.html", {"message": "Proveedor actualizado con éxito"})
    
    else:

      return render(req, "inicio.html", {"message": "Datos inválidos"})
  
  else:

    proveedor = Proveedor.objects.get(id=id)

    formulario = ProvFormulario(initial={
      "codigo": proveedor.codigo,
      "nombre": proveedor.nombre,
      "telefono": proveedor.telefono,
      "email": proveedor.email,     
    })

    return render(req, "editar_proveedor.html", {"formulario": formulario, "id": proveedor.id})


## Producto vistas

class ProdList(LoginRequiredMixin, ListView):

  model = Producto
  template_name = 'prod_list.html'
  context_object_name = "productos"

  def get_queryset(self):
    proveedor_email = self.kwargs.get("proveedor_email")
    proveedor = Proveedor.objects.get(email=proveedor_email)
    
    return proveedor.productos.all()

class ProdDetail(DetailView):

  model = Producto
  template_name = 'prod_detail.html'
  context_object_name = "producto"

class ProdCreate(CreateView):

  model = Producto
  template_name = 'producto_create.html'
  fields = ["nombre", "marca", "precio_costo", "tipo"]
  success_url = "/comp-app/"

class ProdUpdate(UpdateView):

  model = Producto
  template_name = 'producto_update.html'
  fields = ('__all__')
  success_url = "/comp-app/"  
  context_object_name = "producto"

class ProdDelete(DeleteView):

  model = Producto
  template_name = 'producto_delete.html'
  success_url = "/comp-app/"
  
  context_object_name = "producto"

  
## Compras

def compra(nro, fecha_compra,  cantidad, precio_venta):

  nueva_comp = Compra(nro=nro, fecha_compra=fecha_compra, cantidad=cantidad, precio_venta=precio_venta)
  nueva_comp.save()

  return HttpResponse(f"""
    <p>Código: {nueva_comp.nro} - Nombre: {nueva_comp.fecha_compra} creada!</p>
  """)


def compra_formulario(req):

  print('method: ', req.method)
  print('POST: ', req.POST)

  if req.method == 'POST':

    formulario = CompraFormulario(req.POST)

    if formulario.is_valid():

      data = formulario.cleaned_data
      
      nueva_comp = Compra(
                nro=data['nro'],
                fecha_compra=data['fecha_compra'],                
                cantidad=data['cantidad'],
                precio_venta=data['precio_venta'],                
            )
      nueva_comp.save()

      return render(req, TEMPLATE_INICIO, {"message": "Compra creada con éxito"})
    
    else:

      return render(req, TEMPLATE_INICIO, {"message": "Datos inválidos"})
  
  else:

    formulario = CompraFormulario()

    return render(req, "compra_formulario.html", {"formulario": formulario})
  

def compras(req, page=0):

  cant_por_pagina = 3
  total_compras = Compra.objects.count()
  max_page = (total_compras - 1) // cant_por_pagina  


  if req.GET.get('direccion') == 'next'  and page < max_page:
    page += 1
  elif req.GET.get('direccion') == 'previous'  and page > 0:  
    page -= 1

  inicio = int(page) * cant_por_pagina
  final = (int(page)+1) * cant_por_pagina
  
  lista = Compra.objects.all()[inicio:final]

  return render(req, "compras.html", {"lista_compras": lista, "current_page": page,"max_page": max_page})




## AUTENTICACIÓN

def login_view(req):

  if req.method == 'POST':

    formulario = AuthenticationForm(req, data=req.POST)

    if formulario.is_valid():

      data = formulario.cleaned_data

      usuario = data["username"]
      psw = data["password"]

      user = authenticate(username=usuario, password=psw)

      if user:
        login(req, user)
        return render(req, "inicio.html", {"message": f"Bienvenido {usuario}"})
      
      else:
        return render(req, "inicio.html", {"message": "Datos erroneos"})
    
    else:
      return render(req, "inicio.html", {"message": "Datos inválidos"})
  
  else:
    formulario = AuthenticationForm()
    return render(req, "login.html", {"formulario": formulario})
  

def register(req):
    if req.method == 'POST':
        formulario = CustomUserCreationForm(req.POST)
        if formulario.is_valid():
            data = formulario.cleaned_data
            usuario = formulario.save(commit=False)
            usuario.is_staff = data["is_staff"]
            usuario.save()
            return render(req, "inicio.html", {"message": f"Usuario {usuario.username} creado con éxito!"})
        else:
            return render(req, "inicio.html", {"message": "Datos inválidos"})
    else:
        formulario = CustomUserCreationForm()
        return render(req, "registro.html", {"formulario": formulario})



@login_required
def editar_perfil(req):
    usuario = req.user
    if req.method == 'POST':
        formulario = UserEditForm(req.POST, instance=usuario)
        if formulario.is_valid():
            data = formulario.cleaned_data
            usuario.first_name = data["first_name"]
            usuario.last_name = data["last_name"]
            usuario.email = data["email"]
            if data["password1"]:
                usuario.set_password(data["password1"])
            usuario.is_staff = data["is_staff"]
            usuario.save()
            return render(req, "inicio.html", {"message": "Datos actualizados con éxito"})
        else:
            return render(req, "editar_perfil.html", {"formulario": formulario})
    else:
        formulario = UserEditForm(instance=usuario)
        return render(req, "editar_perfil.html", {"formulario": formulario})
  
@login_required
def agregar_avatar(req):

  if req.method == 'POST':

    formulario = AvatarFormulario(req.POST, req.FILES)

    if formulario.is_valid():

      data = formulario.cleaned_data

      avatar = Avatar(user=req.user, imagen=data["imagen"])
      avatar.save()

      return render(req, "inicio.html", {"message": "Avatar cargado con éxito"})
    
    else:

      return render(req, "inicio.html", {"message": "Datos inválidos"})
  
  else:

    formulario = AvatarFormulario()

    return render(req, "agregar_avatar.html", {"formulario": formulario})
    