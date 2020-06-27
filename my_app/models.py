from django.db import models


class News(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    images = models.ImageField(upload_to='')
    # created_by = models.

    create_date = models.DateTimeField(auto_now_add=True)


class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    message = models.TextField()
