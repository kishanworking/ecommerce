from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # for makeing account activate of users
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]