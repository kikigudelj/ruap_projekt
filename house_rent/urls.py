from django.urls import path
from house_rent import views

urlpatterns = [
    path("", views.home, name="home"),
    path("house_rentals/", views.house_rentals, name="house_rentals"),
    path("house/<int:house_id>", views.house_detail, name="house_detail"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('rent_your_house/', views.rent_your_house, name='rent_your_house'),
    path('result/', views.rent_house_predict, name='result'),
    path('predict/', views.rent_house_predict, name='predict'),
]
