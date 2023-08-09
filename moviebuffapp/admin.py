from django.contrib import admin
from .models import MovieDetails,Review,Tag,Artist

# Register your models here.
admin.site.register(MovieDetails)
admin.site.register(Artist)
admin.site.register(Review)
admin.site.register(Tag)

