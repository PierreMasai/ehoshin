from django import forms
from .models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'is_private', 'is_closed')

    def save(self, commit=True):
        import sys
       # print(self.fields['is_private'].__dict__, file=sys.stderr)
        return self.instance
