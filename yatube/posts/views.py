from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Group, Post, User
from .form import PostForm


def index(request):
    '''для главной страницы'''
    posts = Post.objects.all()[:10]
    # Показывать по 10 записей на странице.
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    template = "posts/index.html"
    text = "Это главная страница проекта Yatube"
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "posts": posts,
        "text": text,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    '''для страницы, на которой будут посты, отфильтрованные по группам.'''
    group = get_object_or_404(Group, slug=slug)
    template = "posts/group_list.html"
    text = "Здесь будет информация о группах проекта Yatube"
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        "group": group,
        "posts": posts,
        "text": text
    }
    return render(request, template, context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    context = {
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    context = {
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method != "POST":
        form = PostForm(request.POST)
        return render(request, "new.html", {"form": form})
    form = PostForm(request.POST)
    if not form.is_valid():
        return render(request, "new.html", {"form": form})
    post = form.save(commit=False)
    username = request.user.username
    post.author = User.objects.get(username=username)
    post.save()
    return redirect("index")


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    if post.author != request.user:
        return redirect(
            'post',
            post_id=post.id,
            username=post.author.username
        )
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect(
            'post',
            post_id=post.id,
            username=post.author.username
        )
    return render(
        request,
        'posts/new.html',
        {
            'form': form,
            'title': 'Редактировать запись',
            'button': 'Сохранить запись',
            'post': post
        }
    )
