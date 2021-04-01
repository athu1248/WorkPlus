from users.models import Account
from django.db import models

# Create your models here.

# stores authentication details of the user'S fitbit API connection
class FitBitUser(models.Model):
    user_id = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    access_token = models.TextField()
    expires_in = models.IntegerField()
    refresh_token = models.TextField()
    scope = models.TextField()
    token_type = models.TextField()
    fitbit_user_id = models.TextField()

    def __str__(self):
        return f'{self.user_id.username} FitBit'
