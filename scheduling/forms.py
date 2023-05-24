from .models import *

class LearningGroupForm(forms.ModelForm):
    name = forms.CharField(required=True)
    language = forms.ModelChoiceField(queryset=Language.objects.all())

    class Meta:
        model = LearningGroup
        fields = ['name', 'language']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_teacher = forms.BooleanField(required=False, widget=forms.CheckboxInput)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'is_teacher')
