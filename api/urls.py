from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("categorys", views.CategoryViewSet)
router.register("carts", views.CartViewSet)


# products/{product_pk}/reviews/[{reviews_pk}]
# parent/lookup/child
product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

# carts/cart_pk/cartitems/pk
cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", views.CartItemViewSet, basename="cart-items")


# urlpatterns = router.urls

urlpatterns = [ 
    path("", include(router.urls)),
    path("", include(product_router.urls)),
    path("", include(cart_router.urls)),
    #     path("products/", views.ProductsAPIView.as_view()),
    #     path("products/<uuid:pk>/", views.ProductAPIView.as_view()),
    #     path("categorys", views.CategorysView.as_view()),
    #     path("categorys/<uuid:pk>", views.CategoryView.as_view()),
]
