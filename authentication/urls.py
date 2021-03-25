from django.urls import path, include
from . import views

urlpatterns = [
    path('sign_up/',views.SignUp.as_view(), name='signup'),
    path('sign_in/', views.SignIn.as_view(), name='signin'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),


]
