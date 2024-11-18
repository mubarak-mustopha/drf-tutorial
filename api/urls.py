from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.ApiProducts.as_view()),
    path("products/<uuid:pk>", views.ApiProduct.as_view()),
    path("categorys", views.ApiCategorys.as_view()),
    path("categorys/<uuid:pk>", views.ApiCategory.as_view()),
]
