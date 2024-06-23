from django.urls import path
from django.contrib.auth.views import LogoutView
from comprasapp.views import *

urlpatterns = [
    path("", inicio, name='inicio'),    
    path('about/', about, name='about'),

    path('productos/<int:page>/', productos, name='Productos'),
    path('proveedores/<int:page>/', proveedores, name='Proveedores'),
            
    path('producto-formulario/', producto_formulario, name='producto_formulario'), 
    path('lista-productos/', lista_productos, name='ListaProductos'),
    path('lista-proveedores/', lista_proveedores, name='ListaProveedores'),
    
    path('busqueda-marca/', busqueda_marca, name='BusquedaMarca'),
    path('buscar/', buscar, name='BuscarMarca'),  
    path('detalle-producto/<pk>', ProdDetail.as_view(), name='DetalleProducto'),
    path('proveedor-formulario/', proveedor_formulario, name='proveedor_formulario'), 
    path('crea-proveedor/', crea_proveedor, name='CreaProveedor'),
    path('elimina-proveedor/<int:id>', eliminar_proveedor, name='EliminaProveedor'),
    path('edita-proveedor/<int:id>', editar_proveedor, name='EditaProveedor'),
    path('compra-formulario/', compra_formulario, name='compra_formulario'), 

    path('crea-producto/', ProdCreate.as_view(), name='CreaProducto'),
    path('actualiza-producto/<int:pk>', ProdUpdate.as_view(), name='ActualizaProducto'),    
    path('elimina-producto/<int:pk>', ProdDelete.as_view(), name='EliminaProducto'),
        
    
    path('lista-producto/<int:proveedor_email>', ProdList.as_view(), name='ListaProductos'),
    path('detalle-producto/<pk>', ProdDetail.as_view(), name='DetalleProducto'),

    path('compras/<int:page>/', compras, name='Compras'),

    path('signin/', login_view, name='Login'),
    path('signup/', register, name='Registrar'),
    path('logout', LogoutView.as_view(template_name="logout.html"), name='Logout'),
    path('editar-perfil', editar_perfil, name='EditaPerfil'),
    path('agregar-avatar', agregar_avatar, name='AgregarAvatar'),
]
