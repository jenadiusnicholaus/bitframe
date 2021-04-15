from django.urls import path

from products import views

urlpatterns = [
    path('orders/', views.AddToShoppingCartView.as_view()),
    path('add_to_cart/<str:pk>/', views.AddToShoppingCartView.as_view())
]
