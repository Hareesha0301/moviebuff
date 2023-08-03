from django.db import models
from django.db.models import Avg

# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.caption} "

class MovieDetails(models.Model):
    moviename = models.CharField(max_length=255)
    releaseyear= models.IntegerField(null=True)
    languages=models.CharField(null=True,max_length=255)
    tags =models.ManyToManyField(Tag)
    avg_rating = models.FloatField(default=0)

    def __str__(self):
        return self.moviename

  
class Review(models.Model):
    user_name= models.CharField(max_length=120)
    user_email= models.EmailField()
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
        return f"{self.rating} "
    