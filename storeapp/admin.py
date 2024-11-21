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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Cartitems)
admin.site.register(Customer)
admin.site.register(SavedItem)
admin.site.register(Review)
