from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Post, Category, Tag, Comment, NewsletterSubscriber
from .forms import PostForm, CategoryForm, CommentForm, NewsletterForm


# ==========================================
# PUBLIC BLOG VIEWS
# ==========================================

def post_list(request):
    """Main home page with Hero post, category bar, and paginated feed."""
    featured_post = Post.objects.filter(status='published', is_featured=True).first()
    
    # If no explicitly marked featured post, pick the latest published
    if not featured_post:
        featured_post = Post.objects.filter(status='published').first()

    posts_query = Post.objects.filter(status='published')
    if featured_post:
        posts_query = posts_query.exclude(pk=featured_post.pk)

    # Filter by category if param passed
    selected_cat_slug = request.GET.get('category')
    selected_category = None
    if selected_cat_slug:
        selected_category = get_object_or_404(Category, slug=selected_cat_slug)
        posts_query = posts_query.filter(category=selected_category)

    paginator = Paginator(posts_query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    trending_posts = Post.objects.filter(status='published').order_by('-views_count')[:4]
    categories = Category.objects.annotate(active_count=Count('posts', filter=Q(posts__status='published'))).order_by('-active_count')
    tags = Tag.objects.annotate(active_count=Count('posts', filter=Q(posts__status='published'))).filter(active_count__gt=0)[:15]

    context = {
        'featured_post': featured_post,
        'page_obj': page_obj,
        'trending_posts': trending_posts,
        'categories': categories,
        'tags': tags,
        'selected_category': selected_category,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """Article view with comments, like button, and related stories."""
    # Allow logged-in author to preview drafts
    if request.user.is_authenticated:
        post = get_object_or_404(Post, slug=slug)
    else:
        post = get_object_or_404(Post, slug=slug, status='published')

    # Increment view count in session so we don't spam on refresh
    session_key = f'viewed_post_{post.pk}'
    if not request.session.get(session_key, False):
        Post.objects.filter(pk=post.pk).update(views_count=post.views_count + 1)
        post.views_count += 1
        request.session[session_key] = True

    # Handle comments
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    new_comment.parent = Comment.objects.get(id=parent_id)
                except Comment.DoesNotExist:
                    pass
            new_comment.save()
            messages.success(request, "Your comment has been posted successfully!")
            return redirect('blog:post_detail', slug=post.slug)

    # Related posts by category
    related_posts = Post.objects.filter(category=post.category, status='published').exclude(pk=post.pk)[:3]
    if not related_posts.exists():
        related_posts = Post.objects.filter(status='published').exclude(pk=post.pk)[:3]

    context = {
        'post': post,
        'comments': post.approved_comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


@require_POST
def post_like(request, slug):
    """AJAX like button toggle."""
    post = get_object_or_404(Post, slug=slug)
    session_key = f'liked_post_{post.pk}'

    if request.session.get(session_key, False):
        # Unlike
        if post.likes_count > 0:
            post.likes_count -= 1
            post.save(update_fields=['likes_count'])
        request.session[session_key] = False
        liked = False
    else:
        # Like
        post.likes_count += 1
        post.save(update_fields=['likes_count'])
        request.session[session_key] = True
        liked = True

    return JsonResponse({'liked': liked, 'likes_count': post.likes_count})


def category_detail(request, slug):
    """Filter posts by category."""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/category_detail.html', {
        'category': category,
        'page_obj': page_obj,
    })


def tag_detail(request, slug):
    """Filter posts by tag."""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/tag_detail.html', {
        'tag': tag,
        'page_obj': page_obj,
    })


def search_posts(request):
    """Global search across title, excerpt, and content."""
    query = request.GET.get('q', '').strip()
    posts = Post.objects.none()
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query),
            status='published'
        ).distinct()

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/search_results.html', {
        'query': query,
        'page_obj': page_obj,
        'count': posts.count() if query else 0,
    })


@require_POST
def newsletter_subscribe(request):
    """Newsletter subscription handler."""
    email = request.POST.get('email', '').strip()
    if email:
        sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if created:
            messages.success(request, "🎉 Thank you for subscribing to our newsletter!")
        else:
            messages.info(request, "You're already subscribed with this email.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


# ==========================================
# CMS ADMIN PANEL VIEWS (Dedicated Blogger Studio)
# ==========================================

def cms_login_view(request):
    """Custom aesthetic login for the CMS studio."""
    if request.user.is_authenticated:
        return redirect('blog:cms_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'blog:cms_dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please check your credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'cms/login.html', {'form': form})


def cms_logout_view(request):
    """Logout handler."""
    logout(request)
    messages.info(request, "You have been logged out of the CMS.")
    return redirect('blog:post_list')


@login_required
def cms_dashboard(request):
    """Overview dashboard with analytics and quick actions."""
    posts = Post.objects.all()
    total_posts = posts.count()
    published_count = posts.filter(status='published').count()
    drafts_count = posts.filter(status='draft').count()
    
    total_views = posts.aggregate(total=Sum('views_count'))['total'] or 0
    total_likes = posts.aggregate(total=Sum('likes_count'))['total'] or 0
    total_comments = Comment.objects.count()
    pending_comments = Comment.objects.filter(is_approved=False).count()

    recent_posts = posts.order_by('-created_at')[:5]
    recent_comments = Comment.objects.order_by('-created_at')[:5]
    top_posts = posts.order_by('-views_count')[:4]
    categories = Category.objects.annotate(post_count=Count('posts'))

    context = {
        'total_posts': total_posts,
        'published_count': published_count,
        'drafts_count': drafts_count,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'pending_comments': pending_comments,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        'top_posts': top_posts,
        'categories': categories,
    }
    return render(request, 'cms/dashboard.html', context)


@login_required
def cms_post_list(request):
    """Full post management table with status filtering, search, and pagination."""
    status_filter = request.GET.get('status', 'all')
    category_filter = request.GET.get('category', 'all')
    search_query = request.GET.get('q', '').strip()

    posts = Post.objects.all().select_related('category', 'author')

    if status_filter in ['published', 'draft', 'archived']:
        posts = posts.filter(status=status_filter)

    if category_filter and category_filter != 'all':
        posts = posts.filter(category__slug=category_filter)

    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'search_query': search_query,
        'all_categories': all_categories,
        'total_count': posts.count(),
    }
    return render(request, 'cms/post_list.html', context)


@login_required
def cms_post_create(request):
    """Create a new post with live preview editor."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            action = request.POST.get('submit_action', 'publish')
            if action == 'draft':
                post.status = 'draft'
            elif action == 'publish':
                post.status = 'published'
                post.published_at = timezone.now()
            post.save()
            form.save_m2m() # save tags
            form._save_tags(post)
            messages.success(request, f"🎉 Article '{post.title}' created successfully!")
            return redirect('blog:cms_post_list')
        else:
            messages.error(request, "Please review the form errors below.")
    else:
        form = PostForm()

    categories = Category.objects.all()
    return render(request, 'cms/post_form.html', {
        'form': form,
        'is_edit': False,
        'categories': categories,
    })


@login_required
def cms_post_edit(request, pk):
    """Edit an existing post."""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            action = request.POST.get('submit_action')
            if action == 'draft':
                updated_post.status = 'draft'
            elif action == 'publish':
                updated_post.status = 'published'
            updated_post.save()
            form.save_m2m()
            form._save_tags(updated_post)
            messages.success(request, f"Article '{updated_post.title}' updated successfully!")
            return redirect('blog:cms_post_list')
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = PostForm(instance=post)

    categories = Category.objects.all()
    return render(request, 'cms/post_form.html', {
        'form': form,
        'post': post,
        'is_edit': True,
        'categories': categories,
    })


@login_required
def cms_post_delete(request, pk):
    """Delete a post with confirmation."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f"Article '{title}' was permanently deleted.")
        return redirect('blog:cms_post_list')

    return render(request, 'cms/post_confirm_delete.html', {'post': post})


@login_required
@require_POST
def cms_post_toggle_status(request, pk):
    """Fast AJAX toggle between draft and published."""
    post = get_object_or_404(Post, pk=pk)
    if post.status == 'published':
        post.status = 'draft'
    else:
        post.status = 'published'
        if not post.published_at:
            post.published_at = timezone.now()
    post.save(update_fields=['status', 'published_at'])
    return JsonResponse({'status': post.status})


@login_required
def cms_category_list(request):
    """Category management page."""
    categories = Category.objects.annotate(post_count=Count('posts')).order_by('name')
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' created!")
            return redirect('blog:cms_category_list')
        else:
            messages.error(request, "Failed to create category. Ensure the name is unique.")

    return render(request, 'cms/category_list.html', {
        'categories': categories,
        'form': form,
    })


@login_required
def cms_category_delete(request, pk):
    """Delete a category."""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f"Category '{name}' deleted.")
    return redirect('blog:cms_category_list')


@login_required
def cms_comment_list(request):
    """Comment moderation queue."""
    filter_type = request.GET.get('filter', 'all')
    comments = Comment.objects.select_related('post').order_by('-created_at')

    if filter_type == 'pending':
        comments = comments.filter(is_approved=False)
    elif filter_type == 'approved':
        comments = comments.filter(is_approved=True)

    paginator = Paginator(comments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cms/comment_list.html', {
        'page_obj': page_obj,
        'filter_type': filter_type,
        'pending_count': Comment.objects.filter(is_approved=False).count(),
        'approved_count': Comment.objects.filter(is_approved=True).count(),
        'total_count': Comment.objects.count(),
    })


@login_required
@require_POST
def cms_comment_toggle_approval(request, pk):
    """Approve or unapprove comment."""
    comment = get_object_or_404(Comment, pk=pk)
    comment.is_approved = not comment.is_approved
    comment.save(update_fields=['is_approved'])
    return JsonResponse({'is_approved': comment.is_approved})


@login_required
@require_POST
def cms_comment_delete(request, pk):
    """Delete a comment."""
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    messages.success(request, "Comment deleted.")
    return redirect('blog:cms_comment_list')
