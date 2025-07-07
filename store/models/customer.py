from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    objects = models.Manager()


    def register(self):
        return self.save()

    def isExist(self):
        if Customer.objects.filter(email = self.email):
            return True
        return False


    @staticmethod
    def loginByEmail(email):
        try:
            return Customer.objects.get(email = email)
        except:
            return False

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
