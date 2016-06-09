from django.contrib import admin
from .models import Membership, User
from teams.models import Team


class TeamsListFilter(admin.SimpleListFilter):
    """
    This filter will always return a subset of the instances in a Model, either filtering by the
    user choice or by a default value.
    """
    parameter_name = 'team'
    title = 'Teams'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        queryset = Team.objects.all()
        return sorted([(team.id, team.name) for team in queryset], key=lambda t: t[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(team_id=self.value())

        return queryset


class MemberListFilter(admin.SimpleListFilter):

    """
    This filter will always return a subset of the instances in a Model, either filtering by the
    user choice or by a default value.
    """
    parameter_name = 'member'
    title = 'Members'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        queryset = User.objects.all()
        return sorted([(user.id, user.full_name) for user in queryset], key=lambda u: u[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(member_id=self.value())

        return queryset


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'team', 'type')
    list_filter = (TeamsListFilter, MemberListFilter)


admin.site.register(Membership, MembershipAdmin)
