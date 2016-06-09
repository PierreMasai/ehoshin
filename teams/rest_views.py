"""Module containing the rest related views

- *Filter: a class to held the different possibilities of filtering a request.
- *List: a view for listing models or creating a model instance.
- *Detail: a view for retrieving, updating or deleting a model instance.
"""
from rest_framework import generics, filters
from . import serializers, models


class TeamList(generics.ListCreateAPIView):
    """Team view for listing a queryset or creating a model instance."""
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name',)


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    """Team view for retrieving, updating or deleting a model instance."""
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
