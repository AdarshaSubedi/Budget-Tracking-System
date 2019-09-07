from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.
def isPositive(value):
    if value<0:
        raise ValidationError(f"Value must be positive but you entered {value}")

class Income(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True,blank=True)
    date = models.DateField(default=timezone.now)
    rupees = models.FloatField(validators=[isPositive])
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title