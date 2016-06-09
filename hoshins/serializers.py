"""Serializer module.

This module is used as a step between the model and the Rest part.
It aim to serialize the objects before sending them to the user,
as well as to recreate the models from the serialized data.

"""
from rest_framework import serializers
from . import models, utils
from django.core.exceptions import ObjectDoesNotExist
import users
import teams

class ReferenceShipSerializer(serializers.ModelSerializer):
    """A complete referenceship serializer."""
    name = serializers.ReadOnlyField(source='reference.name')
    color = serializers.ReadOnlyField(source='reference.color')

    class Meta:
        model = models.Referenceship
        fields = ('name', 'color', 'index')


class HelpSerializer(serializers.ModelSerializer):
    """A complete help message serializer."""
    user = users.serializers.UserMinimalSerializer()

    class Meta:
        model = models.Help

    def update(self, instance, validated_data):
        """Update the help message.

        Args:
            instance (Help): The message instance.
            validated_data (dict): The new attributes.

        Returns:
            Help: Return the message instance.
        """
        user = validated_data.pop('user')
        validated_data['owner'] = models.User.objects.get(**user)

        return models.update_instance(instance, validated_data)

    def create(self, validated_data):
        """Create a new help message's model.

        Args:
            validated_data (dict): The attributes.

        Returns:
            Help: Returns the message instance.
        """
        user = validated_data.pop('user')
        validated_data['owner'] = models.User.objects.get(**user)

        return self.Meta.model.objects.create(**validated_data)


class ObjectSerializer(serializers.ModelSerializer):
    """A complete object serializer."""
    owner = users.serializers.UserMinimalSerializer()
    belongs_to = teams.serializers.TeamMinimalSerializer()
    references = ReferenceShipSerializer(many=True, source='referenceship_set', required=False, read_only=True)

    class Meta:
        model = models.Object

    def __init__(self, *args, **kwargs):
        self.flatten = kwargs.pop('flatten', True)
        super().__init__(*args, **kwargs)

    @staticmethod
    def convert_nested(data):
        """Deserialize the nested fields.

        Args:
            data (dict): the attributes.

        Returns:
            dict: Return the same dictionary with the nested
                fields deserialized.
        """
        owner = data.pop('owner')
        data['owner'] = models.User.objects.get(**owner)

        team = data.pop('belongs_to')
        data['belongs_to'] = models.Team.objects.get(**team)

        return data

    @staticmethod
    def unflatten(data, context):
        """Unflatten the instance form the serialized form.

        The function is used when the Object is nested in another
        serialized object.

        Args:
            data (dict): The attributes.
            context (dict): Overall information.

        Returns:
            (Object): Return the instance or raise an exception.
        """
        if 'parent' in data and data['parent']:
            data['parent'] = data['parent'].global_id

        data = context['request'].data

        try:
            if 'global_id' in data:
                instance = models.Object.objects.get(pk=data['global_id'])
                serializer = ObjectSerializer(instance, data=data, context=context)
            else:
                serializer = ObjectSerializer(data=data, context=context)
        except ObjectDoesNotExist:
            serializer = ObjectSerializer(data=data, context=context)

        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def reset_references(self, instance):
        references = self.context['view'].request.data.pop('references', [])
        models.Referenceship.objects.filter(object=instance).delete()

        for reference in references:
            index = reference.pop('index')
            reference = models.Reference.objects.get(name=reference['name'])

            referenceship, _ = models.Referenceship.objects.get_or_create(reference=reference,
                                                                          object=instance)
            referenceship.index = index
            referenceship.save()

    def update(self, instance, validated_data):
        """Update the instance with the validated data.

        Args:
            instance (Object): The instance to update.
            validated_data (dict): The new attributes.

        Returns:
            (Object): Return the instance updated.
        """
        validated_data = ObjectSerializer.convert_nested(validated_data)
        self.reset_references(instance)

        return models.update_instance(instance, validated_data)

    def create(self, validated_data):
        """Create a new instance form the serialized data.

        Args:
            validated_data (dict): The attributes.

        Returns:
            (Object): Return the object created.
        """
        validated_data = ObjectSerializer.convert_nested(validated_data)
        new_object = self.Meta.model.objects.create(**validated_data)

        self.reset_references(new_object)
        return new_object


class ObjectMinimalSerializer(serializers.ModelSerializer):
    """Get the global id of the object."""
    class Meta:
        model = models.Object
        fields = ('global_id',)


class HoshinObjectSerializer(ObjectSerializer):
    """Get an hoshin object model by serializing nested fields."""
    object_ptr = ObjectSerializer(read_only=True)

    class Meta:
        model = models.AbstractHoshinObject

    def get_fields(self):
        """Get fields with flatten nested fields.

        Returns:
            dict: Get the serialized object.
        """
        fields = super().get_fields()
        return utils.get_flatten_fields(fields)


class HoshinSerializer(HoshinObjectSerializer):
    """A complete hoshin serializer."""
    class Meta:
        model = models.Hoshin

    def update(self, instance, validated_data):
        """Update the hoshin instance.

        Args:
            instance (Hoshin): The instance to update.
            validated_data (dict): The new attributes.

        Returns:
            Hoshin: Return the instance updated.
        """
        validated_data['object_ptr'] = ObjectSerializer.unflatten(validated_data['object_ptr'], self.context)

        return models.update_instance(instance, validated_data)

    def create(self, validated_data):
        """Create a new instance form the data serialized.

        Args:
            validated_data (dict): The attributes.

        Returns:
            Hoshin: Return the new instance.
        """
        validated_data['object_ptr'] = ObjectSerializer.unflatten(validated_data['object_ptr'], self.context)

        return self.Meta.model.objects.create(**validated_data)


class ItemSerializer(HoshinObjectSerializer):
    """A complete item serializer."""
    class Meta:
        model = models.Item

    def update(self, instance, validated_data):
        """Update the item instance.

        Args:
            instance (Item): The instance to update.
            validated_data (dict): The new attributes.

        Returns:
            Item: Return the instance updated.
        """
        validated_data['object_ptr'] = ObjectSerializer.unflatten(validated_data['object_ptr'], self.context)

        return models.update_instance(instance, validated_data)

    def create(self, validated_data):
        """Create a new instance form the data serialized.

        Args:
            validated_data (dict): The attributes.

        Returns:
            Item: Return the new instance.
        """
        validated_data['object_ptr'] = ObjectSerializer.unflatten(validated_data['object_ptr'], self.context)

        return self.Meta.model.objects.create(**validated_data)


class ImplementationPrioritySerializer(HoshinObjectSerializer):
    """A complete implementation priority serializer."""
    class Meta:
        model = models.ImplementationPriority

    def update(self, instance, validated_data):
        """Update the implementation priority instance.

        Args:
            instance (ImplementationPriority): The instance to update.
            validated_data (dict): The new attributes.

        Returns:
            ImplementationPriority: Return the instance updated.
        """
        validated_data['object_ptr'] = ObjectSerializer.unflatten(validated_data['object_ptr'], self.context)

        return models.update_instance(instance, validated_data)

    def create(self, validated_data):
        """Create a new instance form the data serialized.

        Args:
            validated_data (dict): The attributes.

        Returns:
            ImplementationPriority: Return the new instance.
        """
        validated_data['object_ptr'] = ObjectSerializer.unflatten(validated_data['object_ptr'], self.context)

        return self.Meta.model.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """A complete comment serializer."""
    object_ptr = ObjectSerializer(read_only=True)

    class Meta:
        model = models.Comment

    def update(self, instance, validated_data):
        """Update the comment instance.

        Args:
            instance (Comment): The instance to update.
            validated_data (dict): The new attributes.

        Returns:
            Comment: Return the instance updated.
        """
        validated_data['object_ptr'] = ObjectSerializer.unflatten(validated_data['object_ptr'], self.context)

        return models.update_instance(instance, validated_data)

    def create(self, validated_data):
        """Create a new instance form the data serialized.

        Args:
            validated_data (dict): The attributes.

        Returns:
            Comment: Return the new instance.
        """
        validated_data['object_ptr'] = ObjectSerializer.unflatten(validated_data['object_ptr'], self.context)

        return self.Meta.model.objects.create(**validated_data)

    def get_fields(self):
        """Get fields with flatten nested fields.

        Returns:
            dict: Get the serialized object.
        """
        fields = super().get_fields()
        return utils.get_flatten_fields(fields)
