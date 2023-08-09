from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.caption} "
    
class Artist(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mini_bio =models.TextField(default="Promising Actor")
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"   

    def __str__(self):
        return self.full_name()
    
    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'

class MovieDetails(models.Model):
    moviename = models.CharField(max_length=255)
    releaseyear= models.IntegerField(null=True)
    languages=models.CharField(null=True,max_length=255)
    tags =models.ManyToManyField(Tag)
    avg_rating = models.FloatField(default=0)
    artist = models.ManyToManyField(Artist)

    def __str__(self):
        return self.moviename

CustomUser = get_user_model()
class Review(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)   
    comment=models.TextField(max_length=400)
    movie =models.ForeignKey(MovieDetails, on_delete=models.CASCADE, null=True , related_name ="Reviews")

    def save(self,*args, **kwargs):
        # Get all the reviews for movie
        # compute the average of all the reviews
        super(Review, self).save(*args, **kwargs)
        computed_average=Review.objects.filter(movie=self.movie).aggregate(Avg("rating"))  #{name,rating}
        self.movie.avg_rating = computed_average["rating__avg"]
        self.movie.save()
        

    def __str__(self):
        return f"{self.rating} {self.user.username} {self.movie.id} "
    
    
    