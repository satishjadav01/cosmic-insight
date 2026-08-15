from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('DateofBirth/', views.DateofBirth, name='DateofBirth'),
    path('numbers_role/', views.numbers_role, name='numbers_role'),
    path('marriage_score/', views.marriage_score, name='marriage_score'),
    path('yourplane/', views.yourplane, name='yourplane'),
    path('login/', views.login_view, name='login'),
    path('profile/',views.profile,name = 'profile'),
    path('logout_view/',views.logout_view,name = 'logout_view'),
    path('generate_pdf/',views.calculate_numerology,name = 'generate_pdf'),
    path('otp/', views.otp, name='otp'),
    path('resend/',views.resend_otp,name = 'resend'),
    path('showdata/', views.showdata, name='showdata'),
    path('edit/', views.edit, name='edit'),
]
