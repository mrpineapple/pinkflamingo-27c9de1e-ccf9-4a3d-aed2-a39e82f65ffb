# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.db.models import Avg
from .utils import round_to_ratings_half


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('Author', related_name='books')
    description = models.TextField(blank=True)
    publisher = models.ForeignKey('Publisher')
    isbn = models.CharField(max_length=255)

    def __unicode__(self):
        authors = ', '.join([unicode(a) for a in self.authors.all()])
        return '{} - {}'.format(self.title, authors)

    @property
    def average_rating_full(self):
        """Average of non-zero ratings for this book (or zero if none exist), to one decimal place.

        Will return 0 rating if no ratings exist.
        """
        rating_avg = self.ratings.filter(rating__gt=0).aggregate(Avg('rating'))['rating__avg']
        return round(rating_avg, 1) if rating_avg else 0

    @property
    def average_rating(self):
        """The average rating, the nearest half rating (i.e 2.1 == 2.0 and 2.3 == 2.5)."""
        return round_to_ratings_half(self.average_rating_full)


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Rating(models.Model):
    rating = models.PositiveIntegerField()
    user = models.ForeignKey('auth.User', related_name='ratings')
    book = models.ForeignKey('Book', related_name='ratings')

    def __unicode__(self):
        return '{} - {} by {}'.format(self.rating, self.book, self.user)
