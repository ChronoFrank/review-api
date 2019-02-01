# -*- coding: utf-8 -*-
import json
from django.contrib.auth.models import User
from models import Review
from rest_framework.test import APITestCase


class UserReviewViewTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "test_user_name",
            "password": "123456",
            "first_name": "test name",
            "last_name": "test last name",
            "email": "test@mailinator.com"
        }
        self.user = User.objects.create(**self.user_data)

    def test_user_method_not_allowed(self):
        """
        test try to do a request with a method not allowed to get and 405 error
        """
        response = self.client.delete('/api/v1/users/'.format(self.user.id), {"email": "test@mailinator.com"})
        self.assertEqual(405, response.status_code)

    def test_get_single_user(self):
        """
        test to retrive a single user by id
        """
        response = self.client.get('/api/v1/users/{}/'.format(self.user.id))
        json_data = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, '"id":{}'.format(self.user.id))
        self.assertEqual(self.user_data.get('username'), json_data.get('username'))
        self.assertEqual(self.user_data.get('first_name'), json_data.get('first_name'))
        self.assertEqual(self.user_data.get('email'), json_data.get('email'))
        self.assertEqual(self.user_data.get('last_name'), json_data.get('last_name'))
        self.assertFalse('"password:"' in json_data)

    def test_get_all_users(self):
        """
        test to retrive all users
        """
        user_1 = User.objects.create_user("test1", "test1@earth.com", "super_secret")
        user_2 = User.objects.create_user("test2", "test2@earth.com", "super_secret")
        user_3 = User.objects.create_user("test3", "test3@earth.com", "super_secret")
        response = self.client.get('/api/v1/users/')
        json_data = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json_data), 4)

    def test_create_user(self):
        """
        test to create a new user
        """
        user_data = {
            "username": "test2_user_name",
            "password": "123456",
            "first_name": "test name",
            "last_name": "test last name",
            "email": "test2@mailinator.com"
        }
        response1 = self.client.post('/api/v1/users/', user_data)
        json_data = json.loads(response1.content)
        self.assertEqual(201, response1.status_code)
        response2 = self.client.get('/api/v1/users/{}/'.format(json_data.get('id')))
        self.assertEqual(200, response2.status_code)

    def test_validate_username_useremail_unique(self):
        user_data = {
            "username": "test_user_name",
            "password": "123456",
            "first_name": "test name",
            "last_name": "test last name",
            "email": "test@mailinator.com"
        }
        response = self.client.post('/api/v1/users/', user_data)
        json_data = json.loads(response.content)
        self.assertEqual(400, response.status_code)
        self.assertEqual(json_data.get('email')[0], u'This field must be unique.')
        self.assertEqual(json_data.get('username')[0], u'This field must be unique.')

    def test_validate_user_required_fields(self):
        user_data = {
            "email": "test2@mailinator.com"
        }
        response = self.client.post('/api/v1/users/', user_data)
        json_data = json.loads(response.content)
        self.assertEqual(400, response.status_code)
        self.assertEqual(json_data.get('username')[0], u'This field is required.')
        self.assertEqual(json_data.get('first_name')[0], u'This field is required.')
        self.assertEqual(json_data.get('last_name')[0], u'This field is required.')
        self.assertEqual(json_data.get('password')[0], u'This field is required.')