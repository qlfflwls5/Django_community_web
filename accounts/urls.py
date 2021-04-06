from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<user_id>/', views.profile, name='profile'),
    path('<user_id>/follow/', views.follow, name='follow'),
]
