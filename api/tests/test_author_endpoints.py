# encoding: utf-8
from __future__ import unicode_literals

import logging
import random

from nose.tools import assert_equal

from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from pinkflamingo.models import Author, Book, Publisher


logger = logging.getLogger(__name__)


class TestAuthorEndpoints(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Såm Lake')
        self.publisher = Publisher.objects.create(name='Pubs `R Us')
        self.book = Book.objects.create(
            title='Restock to Success',
            isbn='42424242424242',
            publisher=self.publisher
        )
        self.book = Book.objects.create(
            title='End-cap Management for Smarties',
            isbn='1234567890123',
            publisher=self.publisher
        )
        self.book.authors.add(self.author)
        self.full_data = {
            'name': self.author.name
        }

        self.books_detail_url = reverse('author-books', kwargs={'pk': self.author.pk})
        self.detail_url = reverse('author-detail', kwargs={'pk': self.author.pk})
        self.list_url = reverse('author-list')

    def test_get_author(self):
        """GET /api/author/\d+/ should return the author"""
        response = self.client.get(self.detail_url)
        assert_equal(status.HTTP_200_OK, response.status_code)
        assert_equal(self.author.pk, response.data['pk'])
        assert_equal(self.author.name, response.data['name'])

    def test_get_books_for_author(self):
        """GET /api/author/\d+/books should return the books written by author"""
        response = self.client.get(self.books_detail_url)
        assert_equal(status.HTTP_200_OK, response.status_code)
        # TODO: data is already rendered. The response "looks" right, but I'm missing something.
        # expected_book_count = 2
        # assert_equal(expected_book_count, len(response.data))

    def test_patch_author(self):
        """PATCH /api/author/\d+/ should update the author"""
        expected_name = 'Story-bot'
        response = self.client.patch(self.detail_url, data={'name': expected_name})
        assert_equal(expected_name, response.data['name'])
        assert_equal(status.HTTP_200_OK, response.status_code)

    def test_put_author(self):
        """PUT /api/author/\d+/ should update the author"""
        expected_name = 'Story-bot'
        self.full_data['name'] = expected_name
        response = self.client.put(self.detail_url, data=self.full_data)
        assert_equal(expected_name, response.data['name'])
        assert_equal(expected_name, Author.objects.first().name)

    def test_delete_author(self):
        """DELETE /api/author/\d+/ should delete the author"""
        expected_authors = Author.objects.count() - 1
        response = self.client.delete(self.detail_url)
        assert_equal(status.HTTP_204_NO_CONTENT, response.status_code)
        assert_equal(expected_authors, Author.objects.count())

    def test_post_author(self):
        """POST /api/author/ should create a author"""
        expected_authors = Author.objects.count() + 1
        response = self.client.post(self.list_url, data=self.full_data)
        assert_equal(status.HTTP_201_CREATED, response.status_code)
        assert_equal(expected_authors, Author.objects.count())

    def test_list_author(self):
        """GET /api/author/ should list all authors"""
        num_created = random.randint(5, 10)
        expected_authors = Author.objects.count() + num_created
        for i in range(num_created):
            Author.objects.create(name='Story-bot {}'.format(i))

        response = self.client.get(self.list_url)
        assert_equal(status.HTTP_200_OK, response.status_code)
        assert_equal(expected_authors, len(response.data))
        for author, response_item in zip(Author.objects.all(), response.data):
            assert_equal(author.pk, response_item['pk'])
