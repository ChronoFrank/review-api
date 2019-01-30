# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from serializers import UserReviewSerializer, ReviewSerializer
from models import Review
from django.contrib.auth.models import User


class HelloView(APIView):
    """
       Small APiView to test the jwt token auth.
       When a user makes a GET request with a jtw token as Authorization Header, it should perform an authentication
        and return a status 200, with a username hello message
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, {}!'.format(request.user.username)}
        return Response(data=content, status=status.HTTP_200_OK)


class UserReviewViewset(ModelViewSet):
    """
    Small ViewSet  to handle no admin users

    retrieve:
        Return a serialized user instance.

    list:
        Return all users, ordered by most recently joined.

    create:
        Create a new user.

    """
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserReviewSerializer
    http_method_names = ['get', 'post' ]


class ReviewModelViewSet(ModelViewSet):
    """
        retrieve:
            Return a review instance if the review belongs to the user associated to the jwt token.

        list:
            Return all review instances associated to the jwt token user, ordered by submission date.

        create:
            Create a reivew for a given jwt token associated to a user.

        """
    queryset = Review.objects.all().order_by('submission_date')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return self.queryset.filter(reviewer=self.request.user)

    def create(self, request, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        request.data['reviewer'] = request.user.id
        request.data['ip_address'] = ip_address
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
