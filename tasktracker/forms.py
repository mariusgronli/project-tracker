from django.forms import ModelForm, Textarea
from django import forms
from django.utils.translation import gettext_lazy as _
from tasktracker.models import ProjectModel,TaskModel
from tasktracker.validate import validate_special_char

###### PROJECT MODEL #######
class CreateProjectForm(ModelForm):
    project = forms.CharField(validators=[validate_special_char])
    class Meta:
        model= ProjectModel
        fields =['project','color','description']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 3})
        }

###### Task Model #######
class CreateTaskForm(ModelForm):
    class Meta:
        model=TaskModel
        fields = ('project','task','duration')
        labels = {
            'duration': _('Standard time'),
        }
        help_texts = {
            'duration': _('time format: HH:MM:SS'),
            'project': _('Select the project for this task')
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        print(user)
        self.fields["project"].queryset = (ProjectModel.objects.all().filter(
                user__exact=user)
            )

class AddCustomTimeForm(ModelForm):
    class Meta:
        model=TaskModel
        fields = ('custom_duration',)
        labels = {
            'custom_duration': _('Time'),
        }
        help_texts = {
            'custom_duration': _('time format: HH:MM:SS. To subtract time use "-" infront. E.g: -00:30:00'),
        }

class UpdateTaskForm(ModelForm):
    class Meta:
        model=TaskModel
        fields = ('task','duration')
        labels = {
            'duration': _('Standard time'),
        }
        help_texts = {
            'duration': _('time format: HH:MM:SS'),
        }
