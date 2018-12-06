from django.db import models


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    nameId= models.IntegerField(unique=True)
    
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=50)
    year = models.DateField()
    imbd = models.IntegerField()
    thbd = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.TextField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    


