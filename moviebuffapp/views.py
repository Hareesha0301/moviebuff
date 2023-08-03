from django.shortcuts import redirect
from django.views import View

# Create your views here.
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import MovieDetails , Review
from .forms import ReviewForm ,UserSignupForm
from .utils import is_user_logged_in
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json

class SignUpView(View):
    def post(self, request): 
        details= json.loads(request.body)

        form = UserSignupForm(details)

        if form.is_valid():
            username = form.cleaned_data["username"]
            fname = form.cleaned_data["first_name"]
            lname = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=username):
                return JsonResponse({"message": "Username already exists"})
            
            myuser= User.objects.create_user(username, email ,password)

            myuser.first_name= fname 
            myuser.last_name =lname

            myuser.save()

            return JsonResponse({"message": "User registered successfully!"})
        else:
            return JsonResponse({"error": form.errors}, status=400)

class LoginView(View):
    def post(self, request): 
        logindetails= json.loads(request.body)
        print(logindetails)
        username=logindetails["username"]
        pass1=logindetails["password"]

        user = authenticate(username= username, password=pass1) 
        if user is not None:
            login(request,user)
          
            context={
                "fname":user.first_name
            }
            
            return JsonResponse({"message": "login successfully"})
            
        else:
            
            return JsonResponse({"error": "Invalid Credentials"}, status=401)

class LogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({"message": "Logged out successfully."})
    
'''class IsAuthorizedView(View):
    def get(self, request):
        authorized = request.user.is_authenticated
        return JsonResponse({"authorized": authorized})

class RestrictedView(View):
    @staticmethod
    def is_authorized(request):
        return request.user.is_authenticated

    def get(self, request):
        authorized = self.is_authorized(request)
        return JsonResponse({"authorized": authorized})'''

class PopularMoviesView(View):
    @is_user_logged_in
    def get(self, request, *args, **kwargs):  
        popular_movies = MovieDetails.objects.order_by('avg_rating')[:5] #avg score 
        response_content = []
  
        for movie in popular_movies:
            
            temp = {
                "name": movie.moviename,
                "rating": movie.avg_rating
            }

            response_content.append(temp)

        print(response_content)
        return JsonResponse(response_content, safe=False)

class AllMoviesView(View):
    @is_user_logged_in
    def get(self, request, *args, **kwargs):
        top_movies = MovieDetails.objects.order_by('-releaseyear')
        response_content = []
  
        for movie in top_movies:
            
            temp = {
                "name": movie.moviename,
                "rating": movie.avg_rating,
                "releaseyear":movie.releaseyear
            }

            response_content.append(temp)
        return JsonResponse(response_content, safe=False)

class IndividualMovieView(View): 
    @is_user_logged_in
    def get(self, request, slug):
        moviepost = MovieDetails.objects.get(moviename=slug)
        print(moviepost)
        
        context={ 
            "moviename": moviepost.moviename,
            "rating": moviepost.avg_rating,
            "releaseyear":moviepost.releaseyear
           
        }
        
        return JsonResponse(context) 

    def post(self, request, slug): 
        print("hello")
        review_form = ReviewForm(request.POST)
        moviepost = MovieDetails.objects.get(moviename=slug)
        if review_form.is_valid(): 
            print("Form is valid")
            review = review_form.save(commit=False)
            review.post= moviepost
            review.save()
            return HttpResponseRedirect(reverse("movie_post_detail", args=[slug]))
        else:
            print("form is not valid")
        
        
        context={ 
            "moviename": moviepost.moviename,
            "moviepost_tags" : moviepost.tags.all() ,
            "review_form"  : ReviewForm(),
            "Reviews": moviepost.reviews.all().order_by("-id"),
           
        }
        
        return HttpResponse(context) 

