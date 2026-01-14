from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm


# Create your views here.
def index(request):
    """Главная страница с пагинацией."""
    current_time = timezone.now()

    post_list = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=current_time
    ).select_related('author', 'category', 'location').order_by('-pub_date')

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, id):
    """Страница отдельного поста."""
    current_time = timezone.now()
    post = get_object_or_404(Post, id=id)

    can_view = False

    if request.user == post.author:
        can_view = True

    else:
        current_time = timezone.now()
        can_view = (
            post.is_published
            and post.category.is_published
            and post.pub_date <= current_time
        )

    if not can_view:
        return redirect('blog:index')

    comments = post.comments.all().order_by('created_at')

    form = None
    if request.user.is_authenticated:
        form = CommentForm()

    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


def category_posts(request, category_slug):
    """Страница с постами определенной категории."""
    current_time = timezone.now()

    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )

    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=current_time
    ).select_related('location', 'author').annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)

@login_required
def create_post(request):
    """Создание нового поста."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('users:profile', username=request.user.username)
    else:
        form = PostForm()

    return render(request, 'blog/create.html', {'form': form})

@login_required
def edit_post(request, id):
    """Редактирование существующего поста."""
    post = get_object_or_404(Post, id=id)

    if request.user != post.author:
        return redirect('blog:post_detail', id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            if 'image-clear' in request.POST:
                post.image.delete(save=False)
            form.save()
            return redirect('blog:post_detail', id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/create.html', {'form': form})

@login_required
def delete_post(request, id):
    """Удаление поста."""
    post = get_object_or_404(Post, id=id)

    if request.user != post.author:
        return redirect('blog:post_detail', id=post.id)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')

    form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form': form})

@login_required
def add_comment(request, id):
    """Добавление комментария."""
    post = get_object_or_404(
        Post.objects.filter(
            is_published=True,
            category__is_published=True
        ),
        id=id
    )

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('blog:post_detail', id=post.id)

    return redirect('blog:post_detail', id=post.id)

@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария."""
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)

    if request.user != comment.author:
        messages.error(request, 'Вы не можете редактировать этот комментарий!')
        return redirect('blog:post_detail', id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Комментарий обновлен!')
            return redirect('blog:post_detail', id=post_id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/comment.html', {
        'form': form,
        'comment': comment,
        'post': comment.post,
    })

@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария."""
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)

    if request.user != comment.author:
        messages.error(request, 'Вы не можете удалить этот комментарий!')
        return redirect('blog:post_detail', id=post_id)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Комментарий удален!')
        return redirect('blog:post_detail', id=post_id)

    return render(request, 'blog/comment.html', {
        'comment': comment,
        'post': comment.post,
    })
