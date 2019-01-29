# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from serializers import UserReviewSerializer, ReviewSerializer
from models import Review


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class UserReviewSingUpView(APIView):
    """
    Creates the user.
    """

    def get(self, request):
        serializer = UserReviewSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserReviewSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({"message": "user successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewModelView(APIView):
    """
    creates and retrive reviews for a given user
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Review.objects.filter(reviewer=request.user).order_by('submission_date')
        serializer = ReviewSerializer(queryset, many=True)
        return Response({"reviewer": request.user.username, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        if request.data:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            data = {
                "company_name": request.data.get("company_name"),
                "summary": request.data.get("summary"),
                "title": request.data.get("title"),
                "rating": request.data.get("rating"),
                "ip_address": ip_address,
            }
            serializer = ReviewSerializer(data=data)
            if serializer.is_valid():
                review = serializer.save()
                if review:
                    review.reviewer = request.user
                    review.save()
                    return Response({"message": "review successfully created", "data": serializer.data},
                                    status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Error, no data provided"}, status=status.HTTP_400_BAD_REQUEST)
