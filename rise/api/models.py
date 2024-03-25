from django.db import models


# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Add your custom fields here
    # For example:
    # bio = models.TextField(blank=True)
    # age = models.IntegerField(blank=True, null=True)

    # Add any additional methods or properties here

    age = models.IntegerField(blank=True, null=True)

    class Meta:
        # Specify the table name for the custom user model
        db_table = 'client_user'

class Expenses(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.FloatField()
    description = models.CharField(max_length=255)
    type = models.ForeignKey('ExpenseType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'expenses'

class ExpenseType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'expense_type'

class Suggestions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    suggestion_type = models.ForeignKey('SuggestionType', on_delete=models.CASCADE)
    saved_money = models.IntegerField()
    description = models.TextField()

    class Meta:
        db_table = 'suggestions'

class SuggestionType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'suggestion_type'
