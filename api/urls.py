from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter


from . import views

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("categorys", views.CategoryViewSet)
router.register("carts", views.CartViewSet)

# /products/product_pk/reviews/pk
products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewVeiwSet, basename="product-reviews")

# urlpatterns = router.urls

urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),
    #     path("products/", views.ProductsView.as_view()),
    #     path("products/<uuid:pk>", views.ProductView.as_view()),
    #     path("categorys", views.CategorysView.as_view()),
    #     path("categorys/<uuid:pk>", views.CategoryView.as_view()),
]
