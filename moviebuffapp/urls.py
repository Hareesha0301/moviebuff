from django.urls import path
from . import views

urlpatterns = [
    path('popmovies', views.PopularMoviesView.as_view(), name='popular_movies'),
    path('movies', views.AllMoviesView.as_view(), name='all_movies'),
    path('movies/<slug:slug>', views.IndividualMovieView.as_view(), name='movie_post_detail'),
    path('login', views.LoginView.as_view(), name='login'),
    path('signup', views.SignUpView.as_view() ,name='signup'),
    path('logout', views.LogoutView.as_view(), name='logout'),
]