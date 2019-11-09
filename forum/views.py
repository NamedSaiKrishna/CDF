from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)

from .forms import CommentForm
from .models import Post, Comment


def home(request):
    return render(request, 'forum/home.html')


class PostListView(ListView):
    model = Post
    template_name = 'forum/feed.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10


class TrendListView(ListView):
    model = Post
    template_name = 'forum/trend.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-comments']
    paginate_by = 10


class SearchPostListView(ListView):
    model = Post
    template_name = 'forum/search.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Post.objects.filter(Q(title__icontains=query)
                                       | Q(content__icontains=query)
                                       | Q(author__username__icontains=query)
                                       )
        return Post.objects.none()


class UserPostListView(ListView):
    model = Post
    template_name = 'forum/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/feed'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/feed'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/feed'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.username
            comment.post = post
            comment.save()
            messages.warning(request, f'Approve or remove Your comment to get posted.')
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'forum/add_comment_to_post.html', {'form': form})


def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)
    return redirect('post-detail', pk=comment.post.pk)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post-detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', pk=comment.post.pk)
