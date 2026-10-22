from django import forms
from .models import Post, Category, Tag, Comment, NewsletterSubscriber


class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Add tags separated by comma, e.g. python, webdev, ai'
        }),
        help_text="Separate tags with commas"
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'excerpt',
            'content',
            'featured_image',
            'featured_image_url',
            'status',
            'is_featured',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input text-lg font-bold',
                'placeholder': 'Enter a captivating story title...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Write a brief engaging summary for preview cards...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea font-mono',
                'rows': 16,
                'placeholder': 'Write your story in Markdown or Rich HTML...'
            }),
            'featured_image_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://images.unsplash.com/...'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-file-input'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
            'read_time': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 1
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            current_tags = self.instance.tags.values_list('name', flat=True)
            self.fields['tags_input'].initial = ', '.join(current_tags)

    def save(self, commit=True):
        post = super().save(commit=commit)
        if commit:
            self._save_tags(post)
        return post

    def _save_tags(self, post):
        tags_str = self.cleaned_data.get('tags_input', '')
        post.tags.clear()
        if tags_str:
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                post.tags.add(tag)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'color', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Category Name'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Description...'}),
            'color': forms.TextInput(attrs={'class': 'form-input color-picker-input', 'type': 'color'}),
            'icon': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. laptop, compass, zap, book'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'comment-input', 'placeholder': 'Your Full Name *', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'comment-input', 'placeholder': 'Your Email Address (kept private) *', 'required': True}),
            'content': forms.Textarea(attrs={'class': 'comment-textarea', 'rows': 4, 'placeholder': 'Share your perspective or thoughts on this article...', 'required': True}),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'newsletter-input',
                'placeholder': 'Enter your email address...',
                'required': True
            })
        }
