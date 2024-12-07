from django.urls import path
from SsideApp import views
urlpatterns = [
        path ('dashboard/',views.dashboard,name='dashboard'),
        path ('add_product/',views.add_product,name='add_product'),
        path ('edit_product/<int:id>',views.edit_product,name='edit_product'),
        path ('delete_product/<int:id>',views.delete_product,name='delete_product'),
        path ('productD/',views.productD,name='productD'),
        path ('manage_order/',views.manage_order,name='manage_order'),
        path ('upload_csv/',views.upload_csv,name='upload_csv'),
        path("", views.index, name='index'),
        
]
