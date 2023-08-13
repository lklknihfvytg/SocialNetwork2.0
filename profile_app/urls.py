from django.urls import path
from . import views


app_name = 'profile_app'

urlpatterns = [
    path('friends/<int:user_id>/', views.ListFriends.as_view())
]
