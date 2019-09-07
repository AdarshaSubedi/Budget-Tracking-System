from django.db import models
from django.utils import timezone
from category.models import Category
from django.contrib.auth.models import User
from  django.core.exceptions import ValidationError
# Create your models here.

def isPositive(value):
    if value<0:
        raise ValidationError(f"Value must be greater than 0 but you entered {value}")

class Expenses(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True,null=True)
    bill = models.FileField(upload_to='bill/',blank=True,null=True)
    date = models.DateField(default=timezone.now)
    rupees = models.FloatField(validators=[isPositive])
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title