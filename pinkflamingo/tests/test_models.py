# encoding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from nose.tools import assert_equal

from pinkflamingo.models import Book, Author, Publisher, Rating


class TestAuthor(TestCase):

    def test_author_has_unicode_method(self):
        """book should have a unicode method that works with non-ascii characters"""
        author = Author.objects.create(name='Óoly Y')
        expected_unicode = 'Óoly Y'
        assert_equal(expected_unicode, unicode(author))


class TestPublisher(TestCase):

    def test_publisher_has_unicode_method(self):
        """publisher should have a unicode method that works with non-ascii characters"""
        publisher = Publisher.objects.create(name='Bastei Lübbe')
        expected_unicode = 'Bastei Lübbe'
        assert_equal(expected_unicode, unicode(publisher))


class TestBook(TestCase):
    
    def setUp(self):
        self.author = Author.objects.create(name='Óoly Y')
        self.author2 = Author.objects.create(name='John H. Watson')
        self.publisher = Publisher.objects.create(name='Samsara')
        self.book = Book.objects.create(
            title='The Road of the Rüne',
            isbn='1234567890123',
            publisher=self.publisher,
        )
        self.book.authors.add(self.author)
        self.book.authors.add(self.author2)

        self.user = User.objects.create_user(
            username='A Reader',
            email='hi@example.com',
            password='h0wdy**'
        )

    def test_rating_has_unicode_method(self):
        """rating should have a unicode method that works with non-ascii characters"""
        expected_unicode = '5 - The Road of the Rüne - Óoly Y, John H. Watson by A Reader'
        rating = Rating.objects.create(book=self.book, user=self.user, rating=5)
        assert_equal(expected_unicode, unicode(rating))

    def test_book_has_unicode_method(self):
        """book should have a unicode method that works with non-ascii characters"""
        expected_unicode = 'The Road of the Rüne - Óoly Y, John H. Watson'
        assert_equal(expected_unicode, unicode(self.book))

    def test_average_rating_with_data(self):
        """book.average_rating should return the average "star rating" of the book"""
        expected_rating = 2.5

        Rating.objects.create(book=self.book, user=self.user, rating=1)
        Rating.objects.create(book=self.book, user=self.user, rating=1)
        Rating.objects.create(book=self.book, user=self.user, rating=5)

        assert_equal(expected_rating, self.book.average_rating)

    def test_average_rating_without_data(self):
        """book.average_rating should return 0 if there are no ratings"""
        expected_rating = 0
        assert_equal(expected_rating, self.book.average_rating)

    def test_average_rating_full(self):
        """book.average_rating should return actual average rating of the book"""
        expected_rating = 2.3

        Rating.objects.create(book=self.book, user=self.user, rating=1)
        Rating.objects.create(book=self.book, user=self.user, rating=1)
        Rating.objects.create(book=self.book, user=self.user, rating=5)

        assert_equal(expected_rating, self.book.average_rating_full)
