from django.urls import path
from . import views

urlpatterns = [
   path('registration/', views.RegisterFrame.as_view(), name='frame'),
   path('get_multiple/', views.GetMultipleQuerrySet.as_view())

]
