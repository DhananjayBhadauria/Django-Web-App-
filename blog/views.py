from django.shortcuts import render
from .models import *
from django.views.generic import *
from django.urls import reverse
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin






def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'bpost':posts})

class PostListView(ListView):
    model = Post
    template_name= 'blog/home.html'
    context_object_name= 'bpost'
    ordering = ['-date_posted']
    paginate_by = 3

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']
    

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']
    

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
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False





def about(request):
    return render(request, 'blog/about.html')