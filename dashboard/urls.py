from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('movie/', views.add_movie, name='movie'),
    path('movie/<int:id>/', views.movie, name='movie_page'),
    path('ticket/', views.ticket, name='ticket'),
]
