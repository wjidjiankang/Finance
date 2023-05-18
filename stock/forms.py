from django import  forms
from stock import models

# class TopicForm(forms.ModelForm):
#     class Meta:
#         model = Topic
#         fields = ['text']
#         labels = {'text':''}
#
#
# class EntryForm(forms.ModelForm):
#     class Meta:
#         model = models.Entry
#         fields = ['text']
#         labels = {'text':''}
#         widgets = {

class GetwordForm(forms.ModelForm):
    class Meta:
        model = models.myText
        fields = ['mytext']
        widgets = {'mytext':forms.Textarea(attrs={'cols':100,})}