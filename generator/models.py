from django.db import models
from django.contrib.auth.models import User


class Schema(models.Model):
    schema_name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    schema_json = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.schema_name


class DataSet(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    def __str__(self):
        return self.url
