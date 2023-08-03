from django import forms
from .models import Review
from django import forms
 
 
 
class UserSignupForm(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    

class ReviewForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Review
        exclude=["movie"]
        labels={
            "user_name":"Your Name",
            "user_email": "Your Email", 
            "rating" : "Rating" ,
            "text": "Your Comment" 
        }

