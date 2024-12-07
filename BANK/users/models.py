from django.db import models
class User(models.Model):
    ID = models.IntegerField(primary_key=True)
    Terms_Of_Use = models.CharField(max_length=255)
    Hashed_Password = models.CharField(max_length=30)
    Mother_Surname = models.CharField(max_length=20)
    Money_Left = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    User_Created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'

class Person(models.Model):
    ID = models.AutoField(primary_key=True)
    Phone_Number = models.CharField(max_length=10)
    Documents = models.CharField(max_length=255)
    Email = models.EmailField()

    class Meta:
        db_table = 'person_info'

class Extract(models.Model):
    Time_started = models.AutoField(primary_key=True)
    Money_Used = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    Operation_Type = models.CharField(max_length=255)
    initial_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)