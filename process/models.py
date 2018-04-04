from django.db import models
from django_mysql.models import JSONField, Model

# Create your models here.

class Stock_Price(models.Model):
    ticker = models.CharField(max_length=6)
    id = models.AutoField(primary_key=True)
    price = JSONField()
    class Meta:
        db_table = "Stock_Price"
