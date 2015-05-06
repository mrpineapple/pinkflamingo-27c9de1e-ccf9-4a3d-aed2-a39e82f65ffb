from django.contrib.auth.models import User

from api.serializers import UserSerializer, BookSerializer, PublisherSerializer, AuthorSerializer, \
    RatingSerializer
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from pinkflamingo.models import Book, Publisher, Author, Rating


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @detail_route()
    def books(self, request, pk=None):
        """
        Returns a list of all books for this author
        """
        books = Book.objects.filter(authors__id=pk)
        return Response([BookSerializer(b).data for b in books])


class PublisherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows publishers to be viewed or edited.
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class RatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ratings to be viewed or edited.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
