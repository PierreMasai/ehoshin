"""Module containing the rest related views

- *Filter: a class to held the different possibilities of filtering a request.
- *List: a view for listing models or creating a model instance.
- *Detail: a view for retrieving, updating or deleting a model instance.
"""
from rest_framework import generics, filters
from eHoshin.views import IsOwnerOrReadOnly, \
    IsUser, IsModeratorOrReadOnly, IsMember

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import django_filters
from . import utils, excel_utils, serializers
from hoshins.utils import *
from hoshins import models

class GlobalIdFilter(django_filters.FilterSet):
    """Global id field filter."""
    global_id = django_filters.CharFilter(name="object_ptr__global_id")

    class Meta:
        fields = ['global_id']


class ParentAndIdFilter(GlobalIdFilter):
    """Parent and global id fields filter."""
    parent = django_filters.CharFilter(name="parent")

    class Meta:
        fields = ['parent', 'global_id']


class ItemFilter(ParentAndIdFilter):
    """Filter used alongside with the items."""
    class Meta(ParentAndIdFilter.Meta):
        model = models.Item


class ItemList(generics.ListCreateAPIView):
    """Item view for listing a queryset or creating a model instance."""
    serializer_class = serializers.ItemSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ItemFilter
    permission_classes = (IsModeratorOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all the items
        as determined by the team name portion of the URL.
        """
        return utils.get_team_elements(self.request.user,
                                       self.kwargs['team'],
                                       models.Item)

    def create(self, request, *args, **kwargs):
        """Create a new Item.

        Args:
            request: The context.
            *args: The attributes of the new Item.
            **kwargs: The attributes of the new Item.

        Returns:
            Response: The response given back to the user
        """
        request.data['belongs_to'] = {'name': self.kwargs['team']}
        data = utils.create_model(self, request, *args, **kwargs)
        return utils.create_response(self, data)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """Item view for retrieving, updating or deleting a model instance."""
    serializer_class = serializers.ItemSerializer
    permission_classes = (IsModeratorOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all the items
        as determined by the team name portion of the URL.
        """
        return utils.get_team_elements(self.request.user,
                                       self.kwargs['team'],
                                       models.Item)


class HelpList(generics.ListCreateAPIView):
    """Help view for listing a queryset or creating a model instance."""
    serializer_class = serializers.HelpSerializer
    permission_classes = (IsModeratorOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all the help messages
        as determined by the team name portion of the URL.
        """

        return models.Help.objects.filter(user=self.request.user)


class HelpDetail(generics.RetrieveUpdateDestroyAPIView):
    """Help view for retrieving, updating or deleting a model instance."""
    queryset = models.Help.objects.all()
    serializer_class = serializers.HelpSerializer
    permission_classes = (IsUser,)


class ImplementationPriorityFilter(ParentAndIdFilter):
    """Filter used alongside with the implementation priorities."""
    class Meta(ParentAndIdFilter.Meta):
        model = models.ImplementationPriority


class ImplementationPriorityList(generics.ListCreateAPIView):
    """ImplementationPriority view for listing a queryset or creating a model instance."""
    serializer_class = serializers.ImplementationPrioritySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ImplementationPriorityFilter
    permission_classes = (IsModeratorOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all the hoshins
        as determined by the team name portion of the URL.
        """
        return utils.get_team_elements(self.request.user,
                                       self.kwargs['team'],
                                       models.ImplementationPriority)

    def create(self, request, *args, **kwargs):
        """Create a new Implementation Priority.

        Args:
            request: The context.
            *args: The attributes of the new Implementation Priority.
            **kwargs: The attributes of the new Implementation Priority.

        Returns:
            Response: The response given back to the user
        """
        request.data['belongs_to'] = {'name': self.kwargs['team']}
        data = utils.create_model(self, request, *args, **kwargs)
        return utils.create_response(self, data)


class ImplementationPriorityDetail(generics.RetrieveUpdateDestroyAPIView):
    """ImplementationPriority view for retrieving, updating or deleting a model instance."""
    serializer_class = serializers.ImplementationPrioritySerializer
    permission_classes = (IsModeratorOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all the implementations priorities
        as determined by the team name portion of the URL.
        """
        return utils.get_team_elements(self.request.user,
                                       self.kwargs['team'],
                                       models.ImplementationPriority)


class CommentFilter(ParentAndIdFilter):
    """Filter used alongside with the comments."""
    class Meta(ParentAndIdFilter.Meta):
        model = models.Comment
        fields = ['parent', 'global_id', 'type']


class CommentList(generics.ListCreateAPIView):
    """Comment view for listing a queryset or creating a model instance."""
    serializer_class = serializers.CommentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CommentFilter
    permission_classes = (IsMember,)

    @staticmethod
    def get_object_commented(comment_type, pk):
        if comment_type == 'hoshins':
            obj = get_object_or_404(models.Hoshin, pk=pk)
        elif comment_type == 'items':
            obj = get_object_or_404(models.Item, pk=pk)
        else:
            obj = get_object_or_404(models.ImplementationPriority, pk=pk)

        return obj.object_ptr

    def get_queryset(self):
        """
        This view should return a list of all the comments
        as determined by the team name portion of the URL.
        """
        result = utils.get_team_elements(self.request.user,
                                         self.kwargs['team'],
                                         models.Comment)

        return result
        # return utils.get_personal_comments(self.request.user,
        #                                    self.kwargs['team'],
        #                                    result)

    def create(self, request, *args, **kwargs):
        """Create a new Comment.

        Args:
            request: The context.
            *args: The attributes of the new Comment.
            **kwargs: The attributes of the new Comment.

        Returns:
            Response: The response given back to the user
        """
        request.data['belongs_to'] = {'name': self.kwargs['team']}
        request.data['parent'] = CommentList.get_object_commented(request.data.pop('type_parent'),
                                                                  request.data['parent'])
        request.data['parent'] = request.data['parent'].pk

        data = utils.create_model(self, request, *args, **kwargs)
        return utils.create_response(self, data)

    def list(self, request, *args, **kwargs):
        """List a queryset.

        Args:
            request: The context.
            *args: /
            **kwargs: /

        Returns:
            Response: The response to give back to the user.
        """
        if request.GET and 'type' in request.GET:
            comment_type = request.GET['type']
            pk = request.GET['parent']
            obj = CommentList.get_object_commented(comment_type, pk)

            # comments = utils.get_personal_comments(self.request.user,
            #                                        self.kwargs['team'],
            #                                        obj.comments)

            comments = obj.comments
            serializer = self.get_serializer(comments, many=True)
            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """Comment view for retrieving, updating or deleting a model instance."""
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all the hoshins
        as determined by the team name portion of the URL.
        """
        return utils.get_team_elements(self.request.user,
                                       self.kwargs['team'],
                                       models.Comment)


class HoshinFilter(GlobalIdFilter):
    """Filter used alongside with the hoshins."""
    class Meta(GlobalIdFilter.Meta):
        model = models.Hoshin
        fields = ['global_id', 'id']


class HoshinList(generics.ListCreateAPIView):
    """Hoshin view for listing a queryset or creating a model instance."""
    serializer_class = serializers.HoshinSerializer
    permission_classes = (IsModeratorOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = HoshinFilter

    def get_queryset(self):
        """
        This view should return a list of all the hoshins
        as determined by the team name portion of the URL.
        """
        return utils.get_team_elements(self.request.user,
                                       self.kwargs['team'],
                                       models.Hoshin)

    def create(self, request, *args, **kwargs):
        """Create a new Hoshin.

        Args:
            request: The context.
            *args: The attributes of the new Hoshin.
            **kwargs: The attributes of the new Hoshin.

        Returns:
            Response: The response given back to the user
        """
        request.data['belongs_to'] = {'name': self.kwargs['team']}
        return super().create(request, *args, **kwargs)


class HoshinDetail(generics.RetrieveUpdateDestroyAPIView):
    """Hoshin view for retrieving, updating or deleting a model instance."""
    serializer_class = serializers.HoshinSerializer
    permission_classes = (IsModeratorOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all the hoshins
        as determined by the team name portion of the URL.
        """
        return utils.get_team_elements(self.request.user,
                                       self.kwargs['team'],
                                       models.Hoshin)

    def get(self, request, *args, **kwargs):
        hoshin_id = request.path_info.split('/')[-1]

        if request.GET.get('type', None) == 'application/excel':
            return get_excel_hoshin(hoshin_id, self.kwargs['team'])

        return self.retrieve(request, *args, **kwargs)


def get_excel_hoshin(hoshin_id, team_name):
    """Function to retrieve a hoshin in an excel shape.

    Args:
        hoshin_id (int): the id of the hoshin.
        team_name (str): the name of the team.

    Returns:
        HttpResponse: the data to give back to the client after a request
    """
    hoshin, hoshin_name = excel_utils.hoshin_to_excel(hoshin_id, team_name)
    response = HttpResponse(hoshin.read(), content_type='application/excel')
    response['Content-Disposition'] = 'inline; filename='+hoshin_name
    return response
