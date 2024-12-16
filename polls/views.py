from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegistrationForm, LoginForm, EditProfileForm, DeleteAccountForm, AddPostForm, CommentForm
from django.core.paginator import Paginator
from .models import Post, UserProfile, Comment


def index(request):
    if request.user.is_authenticated:
        post_list = Post.objects.all()
        paginator = Paginator(post_list, 2)

        page_number = request.GET.get('page')  # Получаем номер страницы из параметров запроса
        page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы

        return render(request, 'polls/index.html', {'page_obj': page_obj})
    else:
        return redirect('login')


#Выход
@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


#Регистрация
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, avatar=form.cleaned_data['avatar'], bio=form.cleaned_data['bio'])
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'polls/register.html', {'form': form})


#Авторизация
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Неверный логин или пароль.')
        else:
            messages.error(request, 'Неверный логин или пароль.')
    else:
        form = LoginForm()
    return render(request, 'polls/login.html', {'form': form})


@login_required
def edit_profile(request):
    user = request.user
    user_profile = user.userprofile  # Получаем связанный UserProfile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():  # Проверяем валидность формы
            user = form.save()  # Сохраняем изменения в User
            user_profile.avatar = request.FILES.get('avatar', user_profile.avatar)  # Обновляем аватар, если он загружен
            user_profile.bio = form.cleaned_data.get('bio', user_profile.bio)  # Обновляем bio
            user_profile.save()  # Сохраняем изменения в UserProfile
            return redirect('profile')  # Переход после успешного обновления
    else:
        # Передаем значение bio в форму при GET-запросе
        form = EditProfileForm(instance=user)
        form.fields['bio'].initial = user_profile.bio  # Устанавливаем начальное значение для bio

    return render(request, 'polls/edit_profile.html', {'form': form})


#Удаление аккаунта
@login_required
def delete_profile(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm_delete']:
            request.user.delete()
            logout(request)
            return redirect('index')
    else:
        form = DeleteAccountForm()
    return render(request, 'polls/delete_profile.html', {'form': form})


#Профиль
@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(author=user).annotate(like_count=Count('likes')).order_by('-like_count')
    return render(request, 'polls/profile.html', {'user': user, 'posts': posts})


#Страница не найдена 404
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1> Страница не найдена </h1>")


@login_required
def create_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')  # Переход на страницу со списком постов
    else:
        form = AddPostForm()
    return render(request, 'polls/create_post.html', {'form': form})


def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    return render(request, 'polls/post_detail.html', {'post': post})


@login_required
def edit_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, author=request.user)
    if request.method == 'POST':
        form = AddPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_slug=post.slug)
    else:
        form = AddPostForm(instance=post)
    return render(request, 'polls/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, author=request.user)
    post.delete()
    return redirect('index')


@login_required
def add_comment(request, post_slug, parent_comment_id=None):
    post = get_object_or_404(Post, slug=post_slug)
    parent_comment = get_object_or_404(Comment, id=parent_comment_id) if parent_comment_id else None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.parent_comment = parent_comment
            comment.save()
            return redirect('post_detail', post_slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'polls/add_comment.html', {'form': form, 'post': post, 'parent_comment': parent_comment})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'polls/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    post_slug = comment.post.slug
    comment.delete()
    return redirect('post_detail', post_slug=post_slug)


def like_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Удаляем лайк
    else:
        post.likes.add(request.user)  # Добавляем лайк
    return redirect('post_detail', post_slug=post_slug)
