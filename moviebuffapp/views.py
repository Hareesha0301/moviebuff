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
            return JsonResponse({"message": "login successfully"})
            
        else:
            
            return JsonResponse({"error": "Invalid Credentials"}, status=401)

class LogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({"message": "Logged out successfully."})

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
                "id":movie.id,
                "name": movie.moviename,
                "rating": movie.avg_rating,
                "releaseyear":movie.releaseyear
            }

            response_content.append(temp)
        return JsonResponse(response_content, safe=False)

class IndividualMovieView(View): 
    @is_user_logged_in
    def get(self, request, id):
        moviepost = MovieDetails.objects.get(id=id)
               
        context={ 
            "moviename": moviepost.moviename,
            "rating": moviepost.avg_rating,
            "releaseyear":moviepost.releaseyear          
        }
        
        return JsonResponse(context) 
    
class ReviewView(View):
    @is_user_logged_in
    def get(self, request, id):
        moviepost = MovieDetails.objects.get(id=id)
        print(moviepost)
        print(type(moviepost))
        reviews= Review.objects.filter(movie=moviepost)
        reviewdetails=[]
        
        for review in reviews:
            context={ 

                "username": review.user.username,
                "email": review.user.email,
                "rating":review.rating,
                "comment":review.comment,       
            }
            reviewdetails.append(context)
        return JsonResponse(reviewdetails,safe=False) 
    
    @is_user_logged_in
    def post(self, request,id ):  
        
        if Review.objects.filter(movie=id, user=request.user).count()==0:
            
            review_form = json.loads(request.body)
            moviepost = MovieDetails.objects.get(id=id)
            form = ReviewForm(review_form)
            print(form)
            if form.is_valid(): 
                print("Form is valid")
                review = form.save(commit=False)
                review.movie= moviepost
                review.user = request.user
                review.save()
                return JsonResponse({"message": "Added review successfully"})
            else:
                print("form is not valid")
                print(form.errors)
                print(request.user)
                print(request.body)
                print(review_form)
                return JsonResponse({"error": "Form is not valid"}, status=400)
        else:
            return JsonResponse({"error": "User has already added review "}, status=400)
 

