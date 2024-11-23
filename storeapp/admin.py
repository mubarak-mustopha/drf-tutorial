from django.contrib import admin
from .models import *


# Register your models here.
class ReviewAdmin(admin.TabularInline):
    model = Review
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ReviewAdmin]


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class CartAdmin(admin.ModelAdmin):
    list_display = ["owner", "cart_id", "session_id"]


class CartItemsAdmin(admin.ModelAdmin):
    list_display = ["id", "cart"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Cartitems, CartItemsAdmin)
admin.site.register(Customer)
admin.site.register(SavedItem)
admin.site.register(Review)
