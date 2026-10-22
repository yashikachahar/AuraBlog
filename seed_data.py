import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Comment

def seed():
    print("[*] Starting database seeding...")

    # 1. Create Superuser / Admin
    admin_user, created = User.objects.get_or_create(username='admin', defaults={
        'email': 'admin@aurablog.com',
        'first_name': 'Alexander',
        'last_name': 'Vance',
        'is_staff': True,
        'is_superuser': True,
    })
    admin_user.set_password('adminpassword123')
    admin_user.save()
    print("[+] Admin user created (Username: admin, Password: adminpassword123)")

    # 2. Categories
    cat_ai, _ = Category.objects.get_or_create(
        name='Artificial Intelligence',
        defaults={'description': 'Frontiers in machine learning, LLMs, neural networks, and generative intelligence.', 'color': '#8b5cf6', 'icon': 'brain'}
    )
    cat_web, _ = Category.objects.get_or_create(
        name='Web Engineering',
        defaults={'description': 'Full-stack architectures, modern Python/Django techniques, and resilient frontend systems.', 'color': '#3b82f6', 'icon': 'code'}
    )
    cat_design, _ = Category.objects.get_or_create(
        name='Design & UI/UX',
        defaults={'description': 'Design systems, micro-interactions, typography, and human-centered digital experiences.', 'color': '#ec4899', 'icon': 'palette'}
    )
    cat_cloud, _ = Category.objects.get_or_create(
        name='Cloud Architecture',
        defaults={'description': 'Distributed microservices, containerization, Kubernetes, and high-availability patterns.', 'color': '#06b6d4', 'icon': 'cloud'}
    )
    cat_career, _ = Category.objects.get_or_create(
        name='Productivity & Career',
        defaults={'description': 'Developer ergonomics, engineering leadership, focus rituals, and career acceleration.', 'color': '#10b981', 'icon': 'zap'}
    )
    print("[+] Categories seeded")

    # 3. Tags
    tags = {}
    tag_names = ['python', 'django', 'machine-learning', 'webdev', 'ui-design', 'cloud', 'architecture', 'productivity', 'career']
    for name in tag_names:
        tag_obj, _ = Tag.objects.get_or_create(name=name)
        tags[name] = tag_obj
    print("[+] Tags seeded")

    # 4. Rich Blog Posts
    posts_data = [
        {
            'title': 'The Next Wave of Autonomous Agentic AI: Beyond Simple Prompts',
            'category': cat_ai,
            'tags': [tags['machine-learning'], tags['python'], tags['architecture']],
            'excerpt': 'Why multi-agent coordination, deterministic memory graphs, and feedback loops are transforming software development faster than standard LLMs ever could.',
            'featured_image_url': 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1400&q=80',
            'status': 'published',
            'is_featured': True,
            'views_count': 1420,
            'likes_count': 89,
            'published_at': timezone.now() - timedelta(days=1),
            'content': """## The Evolution of Intelligent Systems

For the past three years, the industry was captivated by simple zero-shot and few-shot completions. But engineers quickly encountered the boundaries of standalone prompt engineering: context window exhaustion, hallucination traps, and stateless execution.

> "True intelligence emerges not from larger weights alone, but from continuous feedback loops and structured reflection."

Today, modern architectures have shifted decisively toward **multi-agent orchestration**. In this paradigm, distinct specialized agents collaborate through typed protocol contracts to decompose multifaceted engineering challenges.

### Core Architectural Pillars

When building autonomous agents for production codebases, three requirements stand above all:

1. **Deterministic State Graphs**: Workflows must be modeled as state machines with clear branch conditions rather than unconstrained loops.
2. **Context Compression**: Rather than feeding raw logs, agents need dynamic summarizers that preserve critical invariants.
3. **Automated Verification**: Every synthesized artifact must undergo automated linting and unit testing before presentation to human reviewers.

```python
# Conceptual Agent Coordinator in Python
class AgentCoordinator:
    def __init__(self, planning_model, execution_model):
        self.planner = planning_model
        self.executor = execution_model
        self.memory = StateGraph()

    async def run_pipeline(self, task_description: str):
        subtasks = await self.planner.decompose(task_description)
        for step in subtasks:
            result = await self.executor.execute_step(step, self.memory)
            self.memory.record_state(step.id, result)
        return self.memory.compile_final_artifact()
```

### Looking Forward

As agentic frameworks mature, software engineering will transition from writing raw line-by-line syntax to designing **evaluation harnesses** and supervisory constraints. Those who master orchestrating agent swarms will build software at unprecedented speed."""
        },
        {
            'title': 'Mastering High-Performance Django: Caching, Async & Query Optimization',
            'category': cat_web,
            'tags': [tags['python'], tags['django'], tags['webdev']],
            'excerpt': 'Practical strategies to scale your Django backend to millions of daily requests without adding needless architectural bloat.',
            'featured_image_url': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80',
            'status': 'published',
            'is_featured': False,
            'views_count': 980,
            'likes_count': 64,
            'published_at': timezone.now() - timedelta(days=3),
            'content': """## Why Django Continues to Dominate in Enterprise Web

Django has powered critical backends for nearly two decades. Despite recurring trends favoring newer micro-frameworks, Django's batteries-included philosophy, battle-tested ORM, and elegant administration tools make it an enduring choice.

### 1. Eliminating the N+1 Query Dilemma

The single most prevalent bottleneck in web applications is the inadvertent triggering of hundreds of sequential queries inside template rendering loops.

```python
# Bad: Triggers 1 query for posts + N queries for authors
posts = Post.objects.all()

# Good: Efficient single SQL JOIN query
posts = Post.objects.select_related('author', 'category').prefetch_related('tags')
```

### 2. Multi-Tiered Caching Strategy

Never recalculate what hasn't changed. By applying cached view fragments and redis-backed object caching, we cut database read operations by up to 92%.

```python
from django.core.cache import cache

def get_trending_articles():
    key = 'global:trending_posts'
    cached = cache.get(key)
    if cached is None:
        cached = list(Post.objects.filter(status='published').order_by('-views_count')[:5])
        cache.set(key, cached, timeout=3600) # 1 hour TTL
    return cached
```

With these disciplined techniques, scaling Django is both cost-effective and remarkably straightforward."""
        },
        {
            'title': 'The Aesthetic Imperative: Why Premium UI and Micro-Interactions Win',
            'category': cat_design,
            'tags': [tags['ui-design'], tags['webdev']],
            'excerpt': 'In an era of generic web templates, intentional typography, calibrated palettes, and fluid motion create irresistible user delight.',
            'featured_image_url': 'https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=1200&q=80',
            'status': 'published',
            'is_featured': False,
            'views_count': 740,
            'likes_count': 51,
            'published_at': timezone.now() - timedelta(days=5),
            'content': """## The Psychology of Digital Elegance

Users form opinions about your digital product within 50 milliseconds. Long before they evaluate backend throughput or query speeds, they sense whether an interface was crafted with care or thrown together from boilerplate defaults.

> "Simplicity is not the lack of clutter, that's simply a consequence of simplicity. Simplicity somehow essentially describes the purpose and place of an object." — Jony Ive

### The Four Pillars of Modern UI Polish

- **Curated Chromatic Harmony**: Avoid pure primary colors (#FF0000, #0000FF). Instead, leverage tailored HSL hues with subtle optical luminance.
- **Glassmorphism & Depth**: Soft blurred backdrops (`backdrop-filter: blur(16px)`) establish visual hierarchy without clutter.
- **Typography With Soul**: Moving away from system fallbacks to humanistic typefaces like *Plus Jakarta Sans* elevates reading comfort.
- **Micro-Animations**: Hover elevations, spring easing, and progress indicators make static pixels feel alive.

Design is not just what it looks like and feels like. Design is how it works."""
        },
        {
            'title': 'Zero-Downtime Deployments with Docker, Traefik, and Modern Cloud VPS',
            'category': cat_cloud,
            'tags': [tags['cloud'], tags['architecture']],
            'excerpt': 'How to deploy and update monolithic web services seamlessly with automated SSL certificates and health check routing.',
            'featured_image_url': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80',
            'status': 'published',
            'is_featured': False,
            'views_count': 610,
            'likes_count': 38,
            'published_at': timezone.now() - timedelta(days=7),
            'content': """## The Resurgence of the Modern VPS

While hyperscaler serverless architectures have their place, modern cloud servers (Hetzner, DigitalOcean, Linode) paired with Docker Compose offer extraordinary performance-to-cost ratios.

### Rolling Containers Seamlessly

By coupling Docker healthchecks with an intelligent reverse proxy like Traefik or Caddy, new containers spin up and accept traffic only when the application responds with HTTP 200 OK.

```yaml
version: '3.8'
services:
  web:
    image: my-app:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 5s
      timeout: 3s
      retries: 5
    deploy:
      update_config:
        order: start-first
        failure_action: rollback
```

This guarantees that your readers never experience a 502 Bad Gateway during deployments."""
        },
        {
            'title': 'The Deep Work Playbook: How Senior Engineers Eliminate Digital Noise',
            'category': cat_career,
            'tags': [tags['productivity'], tags['career']],
            'excerpt': 'Context switching is the silent killer of engineering momentum. Here is how to construct uninterrupted flow blocks that produce exceptional results.',
            'featured_image_url': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80',
            'status': 'published',
            'is_featured': False,
            'views_count': 530,
            'likes_count': 42,
            'published_at': timezone.now() - timedelta(days=10),
            'content': """## The Cognitive Cost of Fragmented Attention

Every time a notification pings or a quick message arrives, cognitive researchers estimate it requires up to 23 minutes to regain deep conceptual immersion in complex code.

### The 4-Hour Daily Monastic Block

High-output programmers don't work 14 hours a day. Instead, they protect 3 to 4 hours of intense, uninterrupted monastic focus:

- **Asynchronous Communication Defaults**: Disable real-time alerts; check messages at batch intervals (11:30 AM and 4:30 PM).
- **Terminal-Driven Workspaces**: Minimizing tab sprawl reduces visual cognitive overhead.
- **Pre-Commit Task Definitions**: Before closing your laptop in the evening, write down the exact function or test you will start tomorrow morning.

Momentum builds on clarity."""
        },
        {
            'title': 'Building Resilient Micro-Frontends: Lessons from Production Migrations',
            'category': cat_web,
            'tags': [tags['webdev'], tags['architecture']],
            'excerpt': 'A balanced analysis of when micro-frontends solve organizational bottlenecks and when they introduce unnecessary tooling friction.',
            'featured_image_url': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1200&q=80',
            'status': 'draft', # Showcase draft post in CMS!
            'is_featured': False,
            'views_count': 120,
            'likes_count': 8,
            'published_at': timezone.now() - timedelta(days=12),
            'content': """## Deconstructing Micro-Frontend Architecture

Splitting monolithic frontends into federated modules allows independent cross-functional teams to deploy without coordination lockstep. However, shared dependencies, styling isolation, and bundle duplication demand rigorous discipline.

This draft explores module federation best practices and caching topologies."""
        }
    ]

    for p_data in posts_data:
        category = p_data.pop('category')
        post_tags = p_data.pop('tags')
        post, _ = Post.objects.get_or_create(
            title=p_data['title'],
            defaults={
                'author': admin_user,
                'category': category,
                **p_data
            }
        )
        post.tags.set(post_tags)
        post.save()

    print("[+] 6 realistic articles seeded (including published spotlight & draft)")

    # 5. Seed realistic comments
    first_post = Post.objects.filter(status='published').first()
    if first_post:
        c1, _ = Comment.objects.get_or_create(
            post=first_post,
            name="Elena Rostova",
            email="elena@techlabs.io",
            defaults={'content': "This article perfectly crystallizes what we experienced transitioning from single prompts to multi-agent swarms. The state graph approach saved us weeks of debugging!"}
        )
        Comment.objects.get_or_create(
            post=first_post,
            name="Alexander Vance (Author)",
            email="admin@aurablog.com",
            parent=c1,
            defaults={'content': "Thank you Elena! Exactly -- without deterministic state transitions, debugging autonomous runs becomes an exercise in frustration."}
        )
        Comment.objects.get_or_create(
            post=first_post,
            name="Marcus Chen",
            email="marcus@dataspring.com",
            defaults={'content': "Could you elaborate more on automated verification gates in a future post? Super insightful breakdown."}
        )
        print("[+] Comments and nested replies seeded")

    print("\n[+] Seeding completed successfully!")

if __name__ == '__main__':
    seed()

