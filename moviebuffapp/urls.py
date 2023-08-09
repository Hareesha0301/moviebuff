from django.urls import path
from . import views

urlpatterns = [
    path('popmovies', views.PopularMoviesView.as_view(), name='popular_movies'),
    path('movies', views.AllMoviesView.as_view(), name='all_movies'),
    path('movies/<int:id>', views.IndividualMovieView.as_view(), name='movie_post_detail'),
    path('movies/<int:id>/reviews', views.ReviewView.as_view(), name='review_detail'),
    path('login', views.LoginView.as_view(), name='login'),
    path('signup', views.SignUpView.as_view() ,name='signup'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('artists/<int:id>', views.ArtistView.as_view(), name='artist_detail'),
]

