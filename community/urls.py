from django.urls import path
from . import views


app_name = 'community'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:review_pk>/', views.detail, name='detail'),
    path('<int:review_pk>/comment', views.comments_create, name='comments_create'),
    path('<int:review_pk>/likes/', views.likes, name='likes'),
    path('<int:review_pk>/likes_index/', views.likes_index, name='likes_index'),
    path('<int:hash_pk>/hashtag/', views.hashtag, name='hashtah'),
]
