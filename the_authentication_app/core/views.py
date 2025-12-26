from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.decorators import role_required
from  accounts.mixins import RoleRequiredMixin
from django.utils.decorators import method_decorator
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views import View
from django.shortcuts import get_object_or_404

@method_decorator(role_required(['admin']), name='dispatch')
class AdminDashboardView(TemplateView):
    template_name = 'core/admin_dashboard.html'


class AdminDashboardView(RoleRequiredMixin, TemplateView):
    allowed_roles = ['admin']
    template_name = 'core/admin_dashboard.html'


class PostListView(ListView):
    model = Post
    template_name = 'core/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'core/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        return redirect('post_detail', pk=pk)
    


class BlogEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'core/blog_edit.html'
    success_url = reverse_lazy('blog_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.role == 'admin'


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'core/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.role == 'admin'