from django.db import models


class Record(models.Model):
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
		return(f"{self.first_name} {self.last_name}")