import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone=models.CharField(max_length=15, blank=True, null=True)
    
    
    def __str__(self):
        return self.username
class Expenses(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.CharField(max_length=100)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']



    
        

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
class Plan(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    target=models.DecimalField(max_digits=10,decimal_places=2)
    date=models.DateField()

    def __str__(self):
        return f"{self.target} by {self.date}"
    
class PlanItems(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan=models.ForeignKey(Plan,on_delete=models.CASCADE)
    category=models.CharField(max_length=100)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    

