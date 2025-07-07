from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)


    @staticmethod
    def getAllCategory():
        return Category.objects.all();


    def __str__(self):
        return self.name