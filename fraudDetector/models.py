from django.db import models

class User(models.Model):
    last_name = models.CharField(max_length=30)
    discount_code = models.CharField(max_length=30)

    def __str__(self):
        return self.last_name

class Address(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        return self.postcode

class CreditCard(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    last_four_digits = models.CharField(max_length=4)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=4)

    def __str__(self):
        return str(self.last_four_digits) + ' - ' + str(self.expiry_month) + '/' + str(self.expiry_year)