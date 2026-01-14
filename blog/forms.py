from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'location', 'category', 'image')
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_pub_date(self):
        """Валидация даты публикации."""
        pub_date = self.cleaned_data.get('pub_date')

        if pub_date:
            pass

        return pub_date

    def clean(self):
        """Дополнительная валидация."""
        cleaned_data = super().clean()

        category = cleaned_data.get('category')
        if category and not category.is_published:
            raise forms.ValidationError('Выбранная категория не опубликована')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    'Изображение не должно превышать 5MB'
                )

            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
            extension = image.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    f'Неподдерживаемый формат. Разрешены: '
                    f'{", ".join(allowed_extensions)}'
                )

        return image


class CommentForm(forms.ModelForm):
    """Форма для комментариев."""
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите ваш комментарий...'
            }),
        }
        labels = {
            'text': 'Текст комментария',
        }
