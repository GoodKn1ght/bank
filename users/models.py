from django.db import models


class User(models.Model):
    ID = models.AutoField(primary_key=True)
    Terms_Of_Use = models.CharField(max_length=255)
    Hashed_Password = models.CharField(max_length=30)
    Mother_Surname = models.CharField(max_length=20)
    Money_Left = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    User_Created = models.DateTimeField(auto_now_add=True)

class Person(models.Model):
    ID = models.AutoField(primary_key=True)
    Phone_Number = models.CharField(max_length=115)
    Documents = models.CharField(max_length=255)
    Email = models.EmailField()

class Extract(models.Model):
    Time_started = models.AutoField(primary_key=True)
    Money_Used = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    Operation_Type = models.CharField(max_length=255)
    initial_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)

class Operation_Olap(models.Model):
    ID = models.AutoField(primary_key=True)
    Money_Used = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    Time_Completed = models.DateTimeField()
    Operation_Type = models.CharField(max_length=255)
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)

class Operation(models.Model):
    ID = models.AutoField(primary_key=True)
    Money_Used = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    Time_Completed = models.DateTimeField()
    Proccessing_Stage = models.CharField(max_length=255)
    Operation_Type = models.CharField(max_length=255)
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)

class Analitics(models.Model):
    ID = models.AutoField(primary_key=True)
    month_year = models.CharField(max_length=255)
    total_spending = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    total_impact_from_employees = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_impact_from_users = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

class Employee(models.Model):
    ID = models.AutoField(primary_key=True)
    Year_Enrolled = models.IntegerField()
    Position = models.CharField(max_length=255)
    Office = models.CharField(max_length=255)


class Example(models.Model):
    ID = models.AutoField(primary_key=True)

class Example1(models.Model):
    ID = models.AutoField(primary_key=True)
