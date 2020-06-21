from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, User
from .models import Profile
from .forms import ProfileForm, ImageForm
import requests

def getCalorie(foodName, user, quantity):
  url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/guessNutrition"

  querystring = {"title":foodName}

  headers = {
      'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
      'x-rapidapi-key': "d303821b0cmsh1f24ec21b7202dbp1979dcjsn15b0b3cd90e8"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)

  profile = Profile.objects.get(name=User.objects.get(id=user.id))
  currentCalorie = profile.calorie
  calorie = float("%.2f" % (currentCalorie - (quantity *  response.json()['calories']['value'])))
  profile.calorie = calorie
  profile.save()
  return quantity * response.json()['calories']['value']

def homeView(request):
  if request.method == 'POST':
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
      img = request.FILES.get('image')
      quantity = form.cleaned_data.get('quantity')
      if quantity == 'Less':
        int_qu = 1
      elif quantity == 'Medium':
        int_qu = 2
      else:
        int_qu = 3
      print('valid')
      calorie = getCalorie(str(img).split('.')[0], request.user, int_qu)
      context = {
        'form': form,
        'food_item': str(img).split('.')[0],
        'calorie_data': "%.2f" % calorie 
      }
      return render(request, 'home.html', context)
  
  form = ImageForm()
  print('Failed')
  return render(request, 'home.html', {'form': form})

class SignupView(generic.CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('profileCreate')
  template_name = 'signup.html'

class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['age','gender','height','weight', 'type']
    success_url = reverse_lazy('home')
    template_name = "profileUpdate.html"

class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profile.html"

class ProfileCreateView(CreateView):
    model = Profile
    template_name = "profileCreate.html"
    fields = ['name', 'age', 'gender', 'height', 'weight', 'type']
    success_url = reverse_lazy('home')

def profileUpdate(request):
  if request.method == 'POST':
    form = ProfileForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data.get('name')
      age = form.cleaned_data.get('age')
      gender = form.cleaned_data.get('gender')
      height = form.cleaned_data.get('height')
      weight = form.cleaned_data.get('weight')
      type = form.cleaned_data.get('type')
      if gender == 'Male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
      else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
      multiplier = 0.0
      if type == 'Very Light':
        multiplier = 1.3
      elif type == 'Light':
        multiplier = 1.55
      elif type == 'Moderate':
        multiplier = 1.65
      elif type == 'Heavy':
        multiplier = 1.80
      else:
        multiplier = 2.00

      calorie = bmr * multiplier

      r = Profile.objects.create(name=User.objects.get(username=name), age=age, gender=gender, height=height, weight=weight, type=type, calorie=float("%.2f" % calorie))
      r.save()

      return HttpResponseRedirect('login')
  else:
    form = ProfileForm()
  
  return render(request, 'profileCreate.html', {'form': form})
