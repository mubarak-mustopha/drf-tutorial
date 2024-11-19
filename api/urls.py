from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("categorys", views.CategoryViewSet)

urlpatterns = router.urls

# urlpatterns = [
#     path("products/", views.ProductsView.as_view()),
#     path("products/<uuid:pk>", views.ProductView.as_view()),
#     path("categorys", views.CategorysView.as_view()),
#     path("categorys/<uuid:pk>", views.CategoryView.as_view()),
# ]
