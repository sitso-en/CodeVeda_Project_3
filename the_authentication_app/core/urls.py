from django.urls import path
from .views import AdminDashboardView, PostListView, PostDetailView, PostCreateView, AddCommentView, BlogDeleteView, BlogEditView

urlpatterns = [
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('blog/<int:pk>/edit/', BlogEditView.as_view(), name='blog_edit'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
]