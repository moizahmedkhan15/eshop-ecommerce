from django.db import models
from .category import Category


class Products(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='uploads/products/')  # Default/cover image
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @staticmethod
    def getAllProducts():
        """
        Returns all products.
        """
        return Products.objects.all()

    @staticmethod
    def getProductsByCategory(category_id):
        """
        Returns products filtered by category ID.
        """
        return Products.objects.filter(category=category_id)


class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='uploads/products/multiple/')

    def __str__(self):
        return f"Image for {self.product.name}"
