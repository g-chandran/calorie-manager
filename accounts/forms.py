from django.forms import Form, TextInput
from django import forms
from crispy_forms.helper import FormHelper

class ProfileForm(Form):
  name = forms.CharField(label='Enter your name', max_length=200)
  age = forms.IntegerField(label='Enter your age')
  gender = forms.CharField(max_length=6, label='Choose your gender', widget=forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')], attrs={'class': 'form-input'}))
  height = forms.FloatField(label='Enter your height')
  weight = forms.FloatField(label='Enter your weight')
  typeSelection = [
      ('Very Light', 'Very Light'),
      ('Light', 'Light'),
      ('Moderate', 'Moderate'),
      ('Heavy', 'Heavy'),
      ('Very Heavy', 'Very Heavy'),
    ]
  type = forms.CharField(label='Choose the type of work you do everyday', 
    widget=forms.Select(choices=typeSelection, attrs={'class': 'form-input'})
  )
  def __init__(self, *args, **kwargs):
    super(ProfileForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()

class ImageForm(Form):
  image = forms.ImageField()
  quantity = forms.CharField(max_length=6, widget=forms.Select(choices=[('Less', 'Less'), ('Medium', 'Medium'), ('Large', 'Large')]))
  def __init__(self, *args, **kwargs):
    super(ImageForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()