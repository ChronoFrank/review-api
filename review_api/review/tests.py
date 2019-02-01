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


class JWTAuthViewsTesCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user("test", "test@mailinator.com", "super_secret")

    def test_invalid_login(self):
        response = self.client.post('/api/v1/access_token/', {"username": "test", "password": "super"})
        json_data = json.loads(response.content)
        self.assertEqual(400, response.status_code)
        self.assertEqual(json_data.get('non_field_errors')[0], u'No active account found with the given credentials')

    def test_generate_access_token(self):
        response = self.client.post('/api/v1/access_token/', {"username": "test", "password": "super_secret"})
        json_data = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertIn('access', json_data.keys())
        self.assertIn('refresh', json_data.keys())

    def test_refresh_access_token(self):
        response1 = self.client.post('/api/v1/access_token/', {"username": "test", "password": "super_secret"})
        json_data1 = json.loads(response1.content)
        response2 = self.client.post('/api/v1/refresh_token/', {"refresh": json_data1.get('refresh')})
        json_data2 = json.loads(response2.content)
        self.assertEqual(200, response2.status_code)
        self.assertIn('access', json_data2.keys())
        self.assertNotIn('refresh', json_data2.keys())


class ReviewViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user("test", "test@mailinator.com", "super_secret")
        response = self.client.post('/api/v1/access_token/', {"username": "test", "password": "super_secret"})
        json_data = json.loads(response.content)
        self.access_token = json_data.get('access')

    def set_api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def set_api_invalid_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken5546321')

    def test_no_authentication_provided(self):
        response = self.client.get('/api/v1/review/hello/')
        json_data = json.loads(response.content)
        self.assertEqual(401, response.status_code)
        self.assertEqual(json_data.get('detail'), u'Authentication credentials were not provided.')

    def test_invalid_authentication(self):
        self.set_api_invalid_authentication()
        response = self.client.get('/api/v1/review/hello/')
        json_data = json.loads(response.content)
        self.assertEqual(401, response.status_code)
        self.assertEqual(json_data.get('code'), u'token_not_valid')
        self.assertEqual(json_data.get('detail'), u'Given token not valid for any token type')

    def test_auth_method_not_allowed(self):
        self.set_api_authentication()
        response = self.client.patch('/api/v1/review/hello/')
        self.assertEqual(405, response.status_code)

    def test_create_review(self):
        self.set_api_authentication()
        data = {
            "title": "test review",
            "rating": 4,
            "company_name": "fake company",
            "summary": "this is a sumary review"
        }
        response = self.client.post('/api/v1/reviews/', json.dumps(data), content_type='application/json')
        json_data = json.loads(response.content)
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.user.username, json_data.get('reviewer_name'))
        self.assertEqual(data.get('title'), json_data.get('title'))
        self.assertEqual(data.get('rating'), json_data.get('rating'))
        self.assertEqual(data.get('company_name'), json_data.get('company_name'))
        self.assertEqual(data.get('summary'), json_data.get('summary'))
        self.assertTrue('submission_date' in json_data.keys())
        self.assertTrue('ip_address' in json_data.keys())

    def test_validate_fields_in_create_review(self):
        self.set_api_authentication()
        data = {
            "title": "test review",
            "rating": 10,
        }
        response = self.client.post('/api/v1/reviews/', json.dumps(data), content_type='application/json')
        json_data = json.loads(response.content)
        self.assertNotEqual(201, response.status_code)
        self.assertEqual(400, response.status_code)
        self.assertEqual(json_data.get('rating')[0], u'"10" is not a valid choice.')
        self.assertEqual(json_data.get('summary')[0], u'This field is required.')
        self.assertEqual(json_data.get('company_name')[0], u'This field is required.')

    def test_get_all_reviews(self):
        self.set_api_authentication()
        reviews = [
            {
                "title": "test1 review",
                "rating": 4,
                "company_name": "fake company",
                "summary": "this is a sumary review1"
            },
            {
                "title": "test2 review",
                "rating": 2,
                "company_name": "fake company",
                "summary": "this is a sumary review3"
            },
            {
                "title": "test3 review",
                "rating": 5,
                "company_name": "fake company",
                "summary": "this is a sumary review3"
            },

        ]
        for data in reviews:
            response = self.client.post('/api/v1/reviews/', json.dumps(data), content_type='application/json')

        response = self.client.get('/api/v1/reviews/')
        json_data = json.loads(response.content)
        self.assertEqual(len(reviews), len(json_data))
