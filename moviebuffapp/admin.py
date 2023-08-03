from django.contrib import admin
from .models import MovieDetails,Review,Tag

# Register your models here.
admin.site.register(MovieDetails)
#admin.site.register(Author)
admin.site.register(Review)
admin.site.register(Tag)

