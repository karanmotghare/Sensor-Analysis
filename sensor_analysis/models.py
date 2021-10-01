from django.db import connections
from django.db import models

# Create your models here.

class Admins(models.Model):   
 
    class Meta:
        db_table = "record"