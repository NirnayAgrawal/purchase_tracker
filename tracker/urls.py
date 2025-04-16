from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_items, name='upload-items'),
    path('', views.item_list, name='item-list'),
    path('delete/<int:purchase_id>/', views.delete_purchase, name='delete-purchase'),
    path('edit/<int:purchase_id>/', views.edit_purchase, name='edit-purchase'),
    path('export/', views.export_purchases_excel, name='export-purchases'),
]
