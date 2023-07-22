from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    title = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    date = models.DateField()
    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return f"{self.book.title} -> {self.stars}"
    
    class Meta:
        unique_together = (('user', 'book'))
        index_together = (('user', 'book'))
