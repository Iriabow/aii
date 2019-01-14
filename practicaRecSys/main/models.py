from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,URLValidator




class User(models.Model):
    def _str_(self):
        return str(self.id)
    
class Book(models.Model):
    ISBN = ISBN = models.TextField(null=True,blank=True)
    title = models.TextField(null=True,blank=True)
    year = models.IntegerField(null=True,blank=True)
    publisher = models.TextField(null=True,blank=True)
    autor= models.TextField(null=True,blank=True)
    ratings = models.ManyToManyField(User, through="Rating",null=True,blank=True)
    def _str_(self):
        return str(self.title)
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    book= models.ForeignKey(Book,on_delete=models.CASCADE,null=True,blank=True)
    ISBN = models.TextField()
    Book_Rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True,blank=True)
    def __str__(self):
        return str(self.rating)