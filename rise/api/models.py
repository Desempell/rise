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