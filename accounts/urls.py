from django.urls import path
from .views import SignupView, ProfileUpdateView, ProfileDetailView, ProfileCreateView, profileUpdate, homeView

urlpatterns = [
    path('', homeView, name='home'),
    path('accounts/signup/', SignupView.as_view(), name='signup'),
    path('accounts/profile/<pk>/update/', ProfileUpdateView.as_view(), name='profileUpdate'),
    path('accounts/profile/<str:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('accounts/profile', profileUpdate, name='profileCreate'),
]
