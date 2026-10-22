from .models import Category, Post

def blog_globals(request):
    categories = Category.objects.all()
    popular_posts = Post.objects.filter(status='published').order_by('-views_count')[:4]
    return {
        'nav_categories': categories,
        'footer_popular_posts': popular_posts,
        'site_name': 'AuraBlog CMS',
        'site_tagline': 'Crafting Stories, Empowering Creators',
    }
