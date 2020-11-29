""" core app tests modules """

from django.test import TestCase
from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework.permissions import IsAuthenticated 
#models
from .models import (Post, Comment, Category, User)


class PostListTestCase(APITestCase):
    """ posts listing view testing test case """
    def test_post_list_view_returns_200(self):
        """ test post listing view return 200 
        (post listing view request) => 200
        """
        response = self.client.get(reverse('core:posts'))
        self.assertEqual(response.status_code, 200)

