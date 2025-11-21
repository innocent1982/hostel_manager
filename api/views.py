from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

class UserView(APIView):

    def get_permissions(self):
        if self.request_method == "POST":
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def post(self, request, *args, **kwargs):
        user_data = request.data 
        serializer = UserSerializer(user_data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data 
            return Response({"data":data}, status=201)
        return Response({"eror":serializer.errors}, status=400)





