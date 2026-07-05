from django.db import models

class Review(models.Model):
    text = models.TextField()
    sentiment = models.CharField(max_length=20)
    category = models.CharField(max_length=30, null=True, blank=True)
    

    def __str__(self):
        return self.text[:50]