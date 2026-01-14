from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.db.models import Count
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from .forms import CreationForm, ProfileEditForm
from blog.models import Post

# Create your views here.
User = get_user_model()


class SignUp(CreateView):
    """Представление для регистрации пользователя."""
    form_class = CreationForm
    success_url = reverse_lazy('blog:index')
    template_name = 'registration/registration_form.html'

    def form_valid(self, form):
        """Отправляем письмо при успешной регистрации."""
        response = super().form_valid(form)

        user = form.save()
        user_email = form.cleaned_data.get('email')

        if user_email:
            subject = 'Добро пожаловать в Blogicum!'
            message = f'''
            Приветствуем вас, {user.username}!

            Спасибо за регистрацию на нашем сайте Blogicum.
            Теперь вы можете публиковать посты, комментировать и общаться
            с другими пользователями.

            С уважением,
            Команда Blogicum
            '''
            from_email = settings.DEFAULT_FROM_EMAIL

            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[user_email],
                fail_silently=False,
            )

        return response


@login_required
def profile_edit(request, username):
    """Представление для редактирования профиля."""
    user = get_object_or_404(User, username=username)

    if request.user != user:
        return redirect('users:profile', username=user.username)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', username=user.username)
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'blog/user.html', {
        'form': form,
        'profile': user,
    })


def profile_view(request, username):
    """Представление для просмотра профиля пользователя."""
    user = get_object_or_404(User, username=username)

    if request.user == user:
        posts_list = Post.objects.filter(author=user).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    else:
        current_time = timezone.now()
        posts_list = Post.objects.filter(
            author=user,
            is_published=True,
            category__is_published=True,
            pub_date__lte=current_time
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/profile.html', {
        'profile': user,
        'page_obj': page_obj,
        'is_owner': request.user == user,
        'now': timezone.now(),
    })
