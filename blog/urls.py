from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Public Blog
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/like/', views.post_like, name='post_like'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
    path('search/', views.search_posts, name='search'),
    path('subscribe/', views.newsletter_subscribe, name='subscribe'),

    # CMS Studio / Admin Panel
    path('cms/login/', views.cms_login_view, name='cms_login'),
    path('cms/logout/', views.cms_logout_view, name='cms_logout'),
    path('cms/', views.cms_dashboard, name='cms_dashboard'),
    path('cms/posts/', views.cms_post_list, name='cms_post_list'),
    path('cms/posts/create/', views.cms_post_create, name='cms_post_create'),
    path('cms/posts/<int:pk>/edit/', views.cms_post_edit, name='cms_post_edit'),
    path('cms/posts/<int:pk>/delete/', views.cms_post_delete, name='cms_post_delete'),
    path('cms/posts/<int:pk>/toggle-status/', views.cms_post_toggle_status, name='cms_post_toggle_status'),
    path('cms/categories/', views.cms_category_list, name='cms_category_list'),
    path('cms/categories/<int:pk>/delete/', views.cms_category_delete, name='cms_category_delete'),
    path('cms/comments/', views.cms_comment_list, name='cms_comment_list'),
    path('cms/comments/<int:pk>/toggle-approval/', views.cms_comment_toggle_approval, name='cms_comment_toggle_approval'),
    path('cms/comments/<int:pk>/delete/', views.cms_comment_delete, name='cms_comment_delete'),
]
