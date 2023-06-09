from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    email_address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.id and self.user_id is None:
            self.user = kwargs.pop('request').user
        super().save(*args, **kwargs)


class Note(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
