from django.db import models

class User(models.Model):
    last_name = models.CharField(max_length=30)
    discount_code = models.CharField(max_length=30)

class Address(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    postcode = models.CharField(max_length=10)

class CreditCard(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    last_four_digits = models.IntegerField()
    expiry_month = models.IntegerField()
    expiry_year = models.IntegerField()