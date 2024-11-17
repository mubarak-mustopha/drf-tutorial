from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.api_products),
    path("products/<uuid:pk>/", views.api_product),
    path("categorys/", views.api_categorys),
    path("categorys/<uuid:pk>/", views.api_category),
]
