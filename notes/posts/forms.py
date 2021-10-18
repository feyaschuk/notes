from django import forms
from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']
        widgets = {
            'text': forms.Textarea,
            'title': forms.TextInput,
             }
        labels = {'text': 'Введите текст',
                  }
        help_texts = {'text': 'Не более 400 символов',
                      }

    def clean_text(self):
        data = self.cleaned_data['text']
        forbidden_word = 'нецензурная лексика'
        if forbidden_word not in data:
            return data
        raise forms.ValidationError('Использование этого слова запрещено - '+ forbidden_word)



