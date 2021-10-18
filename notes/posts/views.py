from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post

User = get_user_model()
POST_PER_LIST = 10

@login_required
def index(request):
    
    post_list = Post.objects.all()
    last_post = post_list.last()
    paginator = Paginator(post_list, POST_PER_LIST)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)    
    return render(request, 'index.html', {'page': page,
                                          'page_number': page_number, 
                                          'last_post': last_post,})

@login_required
def profile(request, username):
    author = get_object_or_404(User, username=username)
    post = author.posts.all()
    paginator = Paginator(post, POST_PER_LIST)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    return render(request, 'profile.html', {
        'author': author,        
        'page': page, 'post': post})

@login_required
def post_view(request, username, post_id):    
    post = get_object_or_404(Post, pk=post_id, author__username=username)    
    posts = post.author.posts.all()    
    return render(request, 'post.html', {
        'posts': posts,
        'author': post.author,
        'post': post,        
        })
  

@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author_id = request.user.id
            new_post.save()
            return redirect('index')

    return render(request, 'new.html', {'form': form})


@login_required
def post_edit(request, username, post_id):
    post_edit = Post.objects.get(pk=post_id, author__username=username)
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post_edit)

    if request.user != post_edit.author:
        return redirect('post', username, post_id)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post', username, post_id)

    return render(request, 'new.html', {'form': form, 'edit': post_edit})


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def post_delete(request, username, post_id):
    post_delete = Post.objects.get(pk=post_id, author__username=username)
    if request.user != post_delete.author:
        return redirect('post', username, post_id)
    post_delete.delete()
    return redirect('profile', username)
