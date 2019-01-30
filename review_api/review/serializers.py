# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from models import Review


class UserReviewSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=32, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=6, max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name']
                    )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ReviewSerializer(serializers.ModelSerializer):
    submission_date = serializers.ReadOnlyField()
    reviewer_name = serializers.ReadOnlyField(source='reviewer.username')
    reviewer = serializers.PrimaryKeyRelatedField(many=False,
                                                  queryset=User.objects.filter(is_superuser=False),
                                                  write_only=True)

    class Meta:
        model = Review
        fields = ('reviewer_name',
                  'reviewer',
                  'title',
                  'rating',
                  'company_name',
                  'summary',
                  'submission_date',
                  'ip_address')
