from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile, ImagePrediction, DiseasePrediction, Traffic


class RegisterForm(UserCreationForm):
    """ 
    Form to create new user in User model, at register page - RegisterView - register.html
    Fields: firstname, lastname, username, email, password1, password2
    """
    
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    """ 
    Form to login, at login page - CustomLoginView - login.html
    Fields: username, password, remember_me
    """
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'User Name',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    """ 
    Form to retrieve and update user's email and username in profile page - ProfileView - profile.html
    Fields: username, email
    """
    
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    """ 
    Form retrieve and update user's profile from Profile model in profile page - ProfileView - profile.html
    Fields: avatar, bio
    """
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

MODALITY_CHOICES= [
    ('xray', 'Xray'),
    ('others', 'Others'),
    ]

class ImagePredictionForm(forms.ModelForm):
    """ 
    Form to create user's image prediction to ImagePredictionModel in prediction history page - ImagePredictionCreate view - prediction_form.html
    Fields: category, input_image
    """
    category = forms.CharField(required=True, label='Modality', widget=forms.Select(attrs={'class': 'form-control'}, choices=MODALITY_CHOICES))
    input_image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    
    class Meta:
        model = ImagePrediction
        fields = ['category', 'input_image']
        exclude = ['user']
        
