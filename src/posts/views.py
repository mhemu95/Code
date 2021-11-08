from django.shortcuts import render, redirect
from .models import Post
from .forms import Postform
from .filters import PostFilter


def home(request):
    blogs = Post.objects.all()
    single = Post.objects.latest('created_on')
    myFilter = PostFilter(request.GET, queryset=blogs)
    blogs = myFilter.qs

    context = {
        'blogs' : blogs, 'single' : single, 'myFilter' : myFilter
    }
    return render(request, 'front/home.html', context)

# panel home
def post_list(request):
    posts = Post.objects.all()
    context = {
        'post_list' : posts
    }
    return render(request, 'back/post_list.html', context)


def post_detail(request, id):
    # In your detail template, you don't need a for loop; As you are just passing one post to the template:
    post = Post.objects.get(id=id)
    comment = post.comment.filter(status=True)
    context = {
        'post': post,
        'comment': comment
    }
    return render(request, 'front/post_detail.html', context)

#CRUD starts here...
def create_post(request):
    form = Postform()
    if request.method == 'POST':
        form = Postform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    context = {
        'form': form,
        'type': 'Create'
    }
    return render(request, 'back/create_post.html', context)


def update_post(request, id):
    post = Post.objects.get(id=id)
    form = Postform(instance=post)
    if request.method == 'POST':
        form = Postform(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    context = {
        'form': form,
        'type': 'Update' 
    }
    return render(request, 'back/create_post.html', context)


def delete_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    context = {
        'post' : post
    }
    return render(request, 'back/delete_post.html', context)


def search(request):
    q = request.GET['q']
    find = Post.objects.filter(title__icontains=q)
    #find = Post.objects.all()
    context = {
        'find': find
    }
    return render(request, 'search.html', context)
