from django.contrib import admin
from .models.products import Products, ProductImage
from .models.category import Category
from .models.customer import Customer
from .models.order import Order, OrderItem

# Inline for uploading multiple images


class ProductImageInline(admin.TabularInline):  # or StackedInline if preferred
    model = ProductImage
    extra = 1  # Show one empty field to add a new image
    fields = ['image']
    verbose_name = "Additional Product Image"
    verbose_name_plural = "Additional Product Images"


class AdminProducts(admin.ModelAdmin):
    list_display = ['name', 'category', 'description', 'price', 'image']
    inlines = [ProductImageInline]  # 👈 Add image inline to Products admin


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


class AdminCustomer(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'phone', 'address', 'total', 'date')
    search_fields = ('customer__first_name', 'customer__email', 'phone')
    list_filter = ('date',)
    readonly_fields = ('total', 'date')
    inlines = [OrderItemInline]


# Register all other models
admin.site.register(Category, AdminCategory)
admin.site.register(Products, AdminProducts)
admin.site.register(Customer, AdminCustomer)
