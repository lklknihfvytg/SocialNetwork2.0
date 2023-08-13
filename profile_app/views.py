from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from .models import User


class ListFriends(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        friends = [friend.first_name for friend in user.friends.all()]
        friends.append({'self.name': user.first_name})
        return Response(friends)
