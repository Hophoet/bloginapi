from django.test import TestCase
from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework.permissions import IsAuthenticated 

from .models import (Post, Comment, Category, User)
# Home page
class PostListTestCase(APITestCase):
    #test that home page returns a 200
    def test_post_list_view_returns_200(self):
        response = self.client.get(reverse('core:posts'))
        self.assertEqual(response.status_code, 200)

