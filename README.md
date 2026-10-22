# AuraBlog CMS - Modern Dynamic Blog & Content Management System

A dynamic, full-featured blogging platform and dedicated CMS studio built with **Python 3**, **Django**, and modern web standards. Designed specifically to solve the content creation and workflow friction experienced by digital writers, developers, and creators.

---

## 🌟 Key Features

### 1. Dynamic Public Blog System
- **Hero Spotlight Section**: Highlight featured stories with gradient glassmorphism overlays and reading time metrics.
- **Topic Filter Bar**: Quick navigation across categories with dynamic post count badges.
- **Article Feed & Pagination**: Responsive grid layout with image hover animations and author metadata.
- **Article Detail Page**:
  - Top reading progress bar synchronized with page scroll.
  - Formatted Markdown and code snippet rendering.
  - Interactive AJAX **Like** button (toggles without page reload).
  - Copy article URL to clipboard with animated toast notification.
  - Threaded discussion / comments system with nested replies.
  - Related stories recommendations by category.
- **Dark & Light Mode**: Fluid theme toggle with `localStorage` persistence.
- **Universal Search**: Modal search (`Ctrl + K` or search icon) matching titles, excerpts, tags, and content.
- **Newsletter Subscription**: Instant newsletter sign-up with feedback toasts.

### 2. Dedicated Blogger CMS Studio (`/cms/`)
- **Analytics Dashboard**: Real-time counters for Total Articles (Live vs. Draft), Total Reads, Reader Likes, and Pending Comments.
- **Top Stories Leaderboard**: Ranking top-performing articles by reader engagement.
- **Post Writing Canvas & Markdown Toolbar**:
  - Live split-view preview rendering markdown in real-time.
  - Word counter and estimated reading time calculator.
  - One-click formatting buttons (H2, H3, Bold, Italic, Quotes, Code snippets, Links, Bullet lists).
  - Draft vs. Published toggle.
  - Direct Image URL or local file upload with instant image preview.
  - Comma-separated tag pills generator.
- **Post Management Grid**: Filter by status (All, Published, Drafts), category, or keyword with one-click status toggle, edit, preview, and delete.
- **Categories Manager**: Add, edit, customize hex badge colors, and delete categories.
- **Discussion Moderation Center**: Approve, reject, or delete user comments.

### 3. Native Django Administration (`/admin/`)
- Full database-level control, user management, and bulk publishing actions.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Pip

### 1. Run Migrations & Seed Database
```powershell
python manage.py migrate
python seed_data.py
```

### 2. Start the Development Server
```powershell
python manage.py runserver 127.0.0.1:8000
```

### 3. Access URLs & Credentials
- **Public Blog**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **CMS Studio**: [http://127.0.0.1:8000/cms/](http://127.0.0.1:8000/cms/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

#### Pre-Configured Demo Credentials:
- **Username**: `admin`
- **Password**: `adminpassword123`
*(A 1-click **Auto-Fill** button is also available on the CMS Login page)*

---

## 📁 Project Architecture

```
Major Project/
├── blog/
│   ├── templatetags/
│   │   └── blog_tags.py       # Custom markdown & read-time filters
│   ├── admin.py               # Django Admin customization & actions
│   ├── apps.py                # App configuration
│   ├── context_processors.py  # Global navigation & category data
│   ├── forms.py               # PostForm, CategoryForm, CommentForm
│   ├── models.py              # Category, Tag, Post, Comment, Newsletter
│   ├── urls.py                # Public & CMS URL routes
│   └── views.py               # Public controllers & CMS studio views
├── core/
│   ├── settings.py            # Project settings, media/static configuration
│   ├── urls.py                # Root routing & static/media serve
│   └── wsgi.py
├── static/
│   ├── css/
│   │   └── main.css           # Glassmorphism, dark/light themes, design system
│   └── js/
│       └── main.js            # Theme switcher, live preview, AJAX likes
├── templates/
│   ├── base.html              # Public master layout
│   ├── blog/                  # Public views (post_list, post_detail, etc.)
│   └── cms/                   # CMS views (dashboard, post_form, post_list, etc.)
├── manage.py
├── seed_data.py               # Sample database generator
└── db.sqlite3
```
