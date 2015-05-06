# encoding: utf-8
from __future__ import unicode_literals

import logging
import random

from nose.tools import assert_equal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from pinkflamingo.models import Book, Author, Publisher, Rating


logger = logging.getLogger(__name__)


class TestBookEndpoints(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Såm Lake')
        self.publisher = Publisher.objects.create(name='Fantastic Flight')
        self.book = Book.objects.create(
            title='Heraldic Wîng',
            isbn='1234567890123',
            publisher=self.publisher)
        self.book.authors.add(self.author)

        self.user_1 = User.objects.create_user(
            username='Rater B',
            email='b_rater@example.com',
            password='my5t3ry',
        )

        self.user_2 = User.objects.create_user(
            username='A rater',
            email='rater_a@example.com',
            password='my5t3ry',
        )

        self.rating_1 = Rating.objects.create(
            rating=3,
            user=self.user_1,
            book=self.book,
        )

        self.rating_2 = Rating.objects.create(
            rating=5,
            user=self.user_2,
            book=self.book,
        )

        self.full_data = {
            'title': self.book.title,
            'isbn': self.book.isbn,
            'description': 'High fantasy',
            'authors': [self.author.pk],
            'publisher': self.publisher.pk,
        }

        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})
        self.list_url = reverse('book-list')

    def test_get_book(self):
        """GET /api/book/\d+/ should return the book"""
        response = self.client.get(self.detail_url)
        assert_equal(status.HTTP_200_OK, response.status_code)
        assert_equal(self.book.pk, response.data['pk'])
        assert_equal(self.book.title, response.data['title'])
        assert_equal(self.book.publisher.pk, response.data['publisher'])
        assert_equal(self.book.average_rating, 4.0)
        assert_equal([a.pk for a in self.book.authors.all()], response.data['authors'])

    def test_patch_book(self):
        """PATCH /api/book/\d+/ should update the book"""
        expected_description = """In a hole there lived a creepy, grey alien named Sonya Grey. Not
        a backward, hot, tall hole, filled with stamps and a greasy smell, nor yet a violent,
        charming, pretty hole with nothing in it to sit down on or to eat: it was an alien-hole,
        and that means shelter.
        """.strip()
        response = self.client.patch(self.detail_url, data={'description': expected_description})
        assert_equal(status.HTTP_200_OK, response.status_code)
        assert_equal(expected_description, response.data['description'])

    def test_put_book(self):
        """PUT /api/book/\d+/ should update the book"""
        expected_description = "Totally informative description"
        self.full_data['description'] = expected_description
        response = self.client.put(self.detail_url, data=self.full_data)
        assert_equal(expected_description, response.data['description'])
        assert_equal(expected_description, Book.objects.first().description)

    def test_delete_book(self):
        """DELETE /api/book/\d+/ should delete the book"""
        expected_books = Book.objects.count() - 1
        response = self.client.delete(self.detail_url)
        assert_equal(status.HTTP_204_NO_CONTENT, response.status_code)
        assert_equal(expected_books, Book.objects.count())

    def test_post_book(self):
        """POST /api/book/ should create a book"""
        expected_count = Book.objects.count() + 1
        response = self.client.post(self.list_url, data=self.full_data)
        assert_equal(status.HTTP_201_CREATED, response.status_code)
        assert_equal(expected_count, Book.objects.count())

    def test_list_book(self):
        """GET /api/book/ should list all books"""
        num_created = random.randint(5, 10)
        expected_books = Book.objects.count() + num_created
        for i in range(num_created):
            Book.objects.create(
                title='The Neverending Series {}'.format(i),
                isbn='111111111111{}'.format(i),
                publisher=self.publisher
            )

        response = self.client.get(self.list_url)

        assert_equal(status.HTTP_200_OK, response.status_code)
        assert_equal(expected_books, len(response.data))
        for book, response_item in zip(Book.objects.all(), response.data):
            assert_equal(book.pk, response_item['pk'])
