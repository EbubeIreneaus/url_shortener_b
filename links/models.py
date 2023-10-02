from django.db import models

# Create your models here.
class Link(models.Model):
	key = models.CharField(max_length=10)
	link = models.URLField()
	qr_src = models.URLField(max_length=30)
	date = models.DateField(auto_now_add=True)