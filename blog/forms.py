from django import forms
from django.forms.models import ModelForm
from mptt.forms import TreeNodeChoiceField

from .models import Category, Comment


class NewCommentForm(ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].required = False
        self.fields['parent'].label = ''
        self.fields['parent'].widget.attrs.update({'class': 'd-none'})

    class Meta:
        model = Comment
        fields = ('name', 'parent', 'email', 'content')
        widgets = {
            "name": forms.TextInput(attrs={"class": "col-sm-12"}),
            "email": forms.TextInput(attrs={"class": "col-sm-12"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),

        }


class PostSearchForm(forms.Form):

    Query = forms.CharField()
    Category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name'))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Category'].required = False
        self.fields['Query'].label = 'Search For'
        self.fields['Category'].label = 'Category'
        self.fields['Query'].widget.attrs.update({'class':'form-control menudd','data-toggle':'dropdown'})