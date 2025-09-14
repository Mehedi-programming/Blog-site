from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hash_otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Otp for{self.user.username}"