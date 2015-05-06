# encoding: utf-8
from __future__ import unicode_literals

import logging
import random

from nose.tools import assert_equal

from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from pinkflamingo.models import Publisher


logger = logging.getLogger(__name__)


class TestPublisherEndpoints(APITestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name='The Education Bros')

        self.full_data = {
            'name': self.publisher.name
        }

        self.detail_url = reverse('publisher-detail', kwargs={'pk': self.publisher.pk})
        self.list_url = reverse('publisher-list')

    def test_get_publisher(self):
        """GET /api/publisher/\d+/ should return the publisher"""
        response = self.client.get(self.detail_url)
        assert_equal(status.HTTP_200_OK, response.status_code)
        assert_equal(self.publisher.pk, response.data['pk'])
        assert_equal(self.publisher.name, response.data['name'])

    def test_patch_publisher(self):
        """PATCH /api/publisher/\d+/ should update the publisher"""
        expected_name = 'We Make Books'
        response = self.client.patch(self.detail_url, data={'name': expected_name})
        assert_equal(status.HTTP_200_OK, response.status_code)
        assert_equal(expected_name, response.data['name'])

    def test_put_publisher(self):
        """PUT /api/publisher/\d+/ should update the publisher"""
        expected_name = 'We Make Books'
        self.full_data['name'] = expected_name
        response = self.client.put(self.detail_url, data=self.full_data)
        assert_equal(expected_name, response.data['name'])
        assert_equal(expected_name, Publisher.objects.first().name)

    def test_delete_publisher(self):
        """DELETE /api/publisher/\d+/ should delete the publisher"""
        expected_publishers = Publisher.objects.count() - 1
        response = self.client.delete(self.detail_url)
        assert_equal(status.HTTP_204_NO_CONTENT, response.status_code)
        assert_equal(expected_publishers, Publisher.objects.count())

    def test_post_publisher(self):
        """POST /api/publisher/ should create a publisher"""
        expected_publishers = Publisher.objects.count() + 1
        response = self.client.post(self.list_url, data=self.full_data)
        assert_equal(status.HTTP_201_CREATED, response.status_code)
        assert_equal(expected_publishers, Publisher.objects.count())

    def test_list_publisher(self):
        """GET /api/publisher/ should list all publishers"""
        num_created = random.randint(5, 10)
        expected_publishers = Publisher.objects.count() + num_created
        for i in range(num_created):
            Publisher.objects.create(name='Book Factory {}'.format(i))

        response = self.client.get(self.list_url)

        assert_equal(status.HTTP_200_OK, response.status_code)
        assert_equal(expected_publishers, len(response.data))
        for publisher, response_item in zip(Publisher.objects.all(), response.data):
            assert_equal(publisher.pk, response_item['pk'])
