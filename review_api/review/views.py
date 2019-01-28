# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from serializers import UserReviewSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import json


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        print request.user
        print request.META.get('REMOTE_ADDR')
        return Response(content)


class UserReviewSingUp(APIView):
    """
    Creates the user.
    """

    def post(self, request, format='json'):
        serializer = UserReviewSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({"message": "user successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)