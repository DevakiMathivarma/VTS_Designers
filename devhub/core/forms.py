from django import forms
from .models import Project
from django import forms
from .models import HiringPost
from django import forms
from .models import Message
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'images', 'project_title', 'category', 'description', 
            'tags', 'visibility', 'license', 'downloadable'
        ]
        widgets = {
            'project_title': forms.TextInput(attrs={'placeholder': 'Enter project title'}),
            'category': forms.Select(),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your project, inspiration, and design process' ,'class': 'custom-textarea'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Add tags (comma separated)'}),
            'license': forms.Select(),
            'visibility': forms.Select(),
            'downloadable': forms.CheckboxInput()
        }


class HiringPostForm(forms.ModelForm):
    class Meta:
        model = HiringPost
        fields = ['reason_for_hire', 'category', 'budget', 'project_description', 'personal_note', 'hiring_for']
        widgets = {
            'reason_for_hire': forms.TextInput(attrs={'placeholder': 'What are you hiring for?'}),
            'category': forms.TextInput(attrs={'placeholder': 'Choose the Categories'}),
            'budget': forms.NumberInput(attrs={'placeholder': 'What is your budget?'}),
            'project_description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the project' ,'class': 'custom-textarea'}),
            'personal_note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a personal note','class': 'custom-textarea'}),
            'hiring_for': forms.RadioSelect(choices=[('Freelancing', 'Freelancing'), ('Company', 'Company')])
        }


class HiringPostForm(forms.ModelForm):
    class Meta:
        model = HiringPost
        fields = ['reason_for_hire', 'category', 'budget', 'project_description', 'personal_note', 'hiring_for']
        widgets = {
            'reason_for_hire': forms.TextInput(attrs={'placeholder': 'What are you hiring for?'}),
            'category': forms.TextInput(attrs={'placeholder': 'Choose the Categories'}),
            'budget': forms.NumberInput(attrs={'placeholder': 'What is your budget?'}),
            'project_description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the project','class': 'custom-textarea'}),
            'personal_note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a personal note'}),
            'hiring_for': forms.RadioSelect(choices=[('Freelancing', 'Freelancing'), ('Company', 'Company')])
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write your message...', 'rows': 4}),
        }

from django import forms
from .models import PythonUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = PythonUser
        fields = ['about_me']  # include other fields too
        widgets = {
    'about_me': forms.Textarea(attrs={'class': 'about-me-textarea'}),
}