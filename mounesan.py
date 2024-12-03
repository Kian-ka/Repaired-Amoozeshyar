from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class ContactInfo(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"Contact info for {self.employee}"
