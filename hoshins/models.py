from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q

from hoshins import utils
from users.models import *

###########
# basics functions
###########


def update_instance(instance, data, commit=True):
    """The function update a db object.

    Args:
        commit (bool): True to save the modification, False otherwise
        instance: A db object to update.
        data (dict): A dictionary with all the attributes to change .

    Returns:
        The instance updated.
    """
    for (key, value) in data.items():
        setattr(instance, key, value)

    if commit:
        instance.save()

    return instance


###########
# validators
###########


def validate_css_color_code(color_code):
    """Check if the css color code is valid.

    Args:
        color_code (str): The color code to validate.

    Raises:
        ValidationError: If the code size is wrong or if there is
            an invalid character.
    """
    hex_digits = set("0123456789ABCDEFabcdef")
    is_hex = all(char in hex_digits for char in color_code[1:])

    if len(color_code) != 7:
        raise ValidationError('%s is not a good color code size (must be 7)' % len(color_code))
    if color_code[0] != '#' or not is_hex:
        raise ValidationError('The color code "%s" is not valid' % color_code)


###########
# models
###########

class Reference(models.Model):
    """The reference model hold the reference documents information.

    A reference is a static hoshin giving the context.
    """
    name = models.CharField(max_length=256)
    color = models.CharField(validators=[validate_css_color_code], max_length=7, default='#81b9c3')
    team = models.ForeignKey(Team, related_name='references')


class Help(models.Model):
    """The help model is used to display temporary message.

    It aim to display information to help the user. The user can
    remove it after acknowledged it.
    """
    type = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='helps')


class Object(models.Model):
    """This model is used to store all the object belonging to an hoshin.

    Those objects can be commented by a user and have a global id to do so.
    """
    global_id = models.AutoField(primary_key=True)
    belongs_to = models.ForeignKey(Team, related_name='hoshins')
    owner = models.ForeignKey(User, blank=True, null=True)
    owner_temp = models.CharField(max_length=2000, blank=True)
    references = models.ManyToManyField(Reference, related_name='reference_of', through='Referenceship', blank=True)

    def delete(self, using=None):
        """Delate all the items... belonging to the hoshin before his deletion.

        Args:
            using: ?
        """
        for comment in self.comments.all():
            comment.delete(using)

        super().delete(using)


class Referenceship(models.Model):
    """A model to have an index per reference."""
    reference = models.ForeignKey(Reference)
    object = models.ForeignKey(Object, null=True)
    index = models.CharField(max_length=50, default="", blank=True)


class AbstractHoshinObject(models.Model):
    """The model is used to hold the common attributes/functions of the hoshin objects.

    An hoshin object is either an Hoshin, or a theme or a concrete action.
    """
    name = models.CharField(max_length=200)
    object_ptr = models.OneToOneField(Object)

    class Meta:
        abstract = True

    def delete(self, using=None):
        """Delete the core model before the current one.

        Args:
            using: ?
        """
        self.object_ptr.delete(using)
        super().delete(using)

    def get_trunc_name(self, trunc=35):
        """Get the truncated name of the model.

        Args:
            trunc (int): The number of character to display

        Returns:
            str: The name truncated if the name if too long, the full name otherwise.
        """
        if len(self.name) > trunc:
            return self. name[:trunc-3] + '...'
        else:
            return self.name


class Hoshin(AbstractHoshinObject):
    """The hoshin model store the hoshin properties.

    It mainly composed by the statistics information.
    """
    id = models.AutoField(primary_key=True)
    color = models.CharField(validators=[validate_css_color_code], max_length=7)

    # Stats
    nb_comments = models.IntegerField(default=0)
    nb_items = models.IntegerField(default=0)
    nb_implementation_priorities = models.IntegerField(default=0)
    nb_participants = models.IntegerField(default=0)
    nb_users = models.IntegerField(default=0)

    # Number of users who commented once
    nb_commentators = models.IntegerField(default=0)

    # Number of users who commented more than once
    nb_chatty_commentators = models.IntegerField(default=0)

    def add_item(self):
        self.nb_items += 1
        self.save()

    def remove_item(self):
        self.nb_items -= 1
        self.save()

    def add_i_p(self):
        self.nb_implementation_priorities += 1
        self.save()

    def remove_i_p(self):
        self.nb_implementation_priorities -= 1
        self.save()

    def add_comment(self, user):
        """Update the statistics before a comment addition.

        Args:
            user (User): The user who wrote a comment.
        """
        self.nb_comments += 1

        nb_cmt = self.get_nb_cmt(user)
        if nb_cmt == 0:
            self.nb_commentators += 1
        elif nb_cmt == 1:
            self.nb_commentators -= 1
            self.nb_chatty_commentators += 1

        self.save()

    def remove_comment(self, user):
        """Update the statistics before a comment deletion.

        Args:
            user (User): The user who deleted a comment.
        """
        self.nb_comments -= 1

        nb_cmt = self.get_nb_cmt(user)
        if nb_cmt == 2:
            self.nb_commentators += 1
            self.nb_chatty_commentators -= 1
        elif nb_cmt == 1:
            self.nb_commentators -= 1

        self.save()

    def get_nb_cmt(self, user):
        """Auxiliary function to get the number of comments wrote by the user.

        To keep in mind that is the number of comments wrote belonging to
        the current hoshin.

        Args:
            user (User): The user who commented.

        Returns:
            int: The number of comments.
        """

        def get_comments(model):
            comments = model.object_ptr.comments.all()
            if hasattr(model, 'children'):
                for child in model.children.all():
                    comments |= get_comments(child)

            return comments

        cms = get_comments(self)

        nb_cmt = 0
        me = user.get_full_name()

        for cm in cms:
            obj_com = cm.object_ptr
            author = obj_com.owner_temp

            if obj_com.owner_temp == "" and obj_com.owner:
                author = obj_com.owner.full_name

            if author == me:
                nb_cmt += 1

        return nb_cmt

    def delete(self, using=None):
        """Delate all the items... belonging to the hoshin before his deletion.

        Args:
            using: ?
        """
        for child in self.children.all():
            child.delete(using)

        super().delete(using)


class Item(AbstractHoshinObject):
    """This model store the items properties.

    It made up of the leader of the item, a text describing the target,
    the aim of the item and the hoshin to which it's tied.
    """
    id = models.AutoField(primary_key=True)
    target = models.CharField(max_length=2000)
    parent = models.ForeignKey('Hoshin', related_name='children')
    leader = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        """Save the model.

        The function call the add_item function to update the statistic if
        it's not an update (i.e: if the pk doesn't exist yet).

        Args:
            *args: The model attributes.
            **kwargs: The model attributes.

        Returns:
            (Item): Return the model created.
        """
        if not self.pk:
            self.parent.add_item()
        return super().save(*args, **kwargs)

    def delete(self, using=None):
        """Delete the children and update the statistics before his deletion.

        Args:
            using: ?
        """
        for child in self.children.all():
            child.delete(using)

        self.parent.remove_item()
        super().delete(using)


# TODO: remove the leader attribute and change the name in ConcreteAction
class ImplementationPriority(AbstractHoshinObject):
    """This model store the implementationPriority (or concrete actions) properties.

    It made up of a text describing the target and the hoshin to which it's tied.
    """
    id = models.AutoField(primary_key=True)
    target = models.CharField(max_length=2000)
    parent = models.ForeignKey('Item', related_name='children')
    leader = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        """Save the model.

        The function call the add_i_p function to update the statistic if
        it's not an update (i.e: if the pk doesn't exist yet).

        Args:
            *args: The model attributes.
            **kwargs: The model attributes.

        Returns:
            (ImplementationPriority): Return the model created.
        """
        if not self.pk:
            self.parent.parent.add_i_p()
        return super().save(*args, **kwargs)

    def delete(self, using=None):
        """Update the statistics before his deletion.

        Args:
            using: ?
        """
        self.parent.parent.remove_i_p()
        super().delete(using)


class Comment(models.Model):
    """This model store the comment properties.

    It made up of the CRUD type of the comment (meaning: if it's a comment to propose
    a deletion, update... or none of them).
    """
    DEFAULT_TYPE = 'NO'
    MODIFICATION = 'MO'
    ADDITION = 'AD'
    REMOVAL = 'RE'

    TYPES = (
                (MODIFICATION, 'Modification'),
                (ADDITION,     'Addition'),
                (REMOVAL,      'Removal'),
                (DEFAULT_TYPE, 'Normal'),
             )

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=2, choices=TYPES, default=DEFAULT_TYPE)
    text = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    object_ptr = models.ForeignKey(Object)

    # The object commented
    parent = models.ForeignKey(Object, related_name='comments')

    # TODO: remove notification if the user didn't saw him before his deletion
    def delete(self, using=None):
        """Delete the core model and update statistics before his deletion.

        Args:
            using: ?
        """
        hoshin = utils.get_hoshin(self.parent)
        hoshin.remove_comment(self.object_ptr.owner)

        self.object_ptr.delete(using)
        super().delete(using)

    def save(self, *args, **kwargs):
        """Save the model.

        The function call the add_comment function to update the statistic if
        it's not an update (i.e: if the pk doesn't exist yet). Moreover, a notification
        is sent to the following users.

        Args:
            *args: The model attributes.
            **kwargs: The model attributes.

        Returns:
            (Comment): Return the model created.
        """
        if not self.pk:
            hoshin = utils.get_hoshin(self.parent)
            hoshin.add_comment(self.object_ptr.owner)
            utils.notify_comment(self, self.object_ptr.belongs_to.name)

        return super().save(*args, **kwargs)
