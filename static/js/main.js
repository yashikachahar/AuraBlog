/**
 * AuraBlog CMS - Interactive JavaScript Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSearchModal();
  initReadingProgressBar();
  initLikeButton();
  initCopyLinkButtons();
  initCmsEditorPreview();
  initCmsStatusToggle();
});

/* ===================================================================
   THEME TOGGLE (Dark / Light)
   =================================================================== */
function initTheme() {
  const themeToggles = document.querySelectorAll('.theme-toggle-btn');
  const savedTheme = localStorage.getItem('aurablog-theme') || 
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

  applyTheme(savedTheme);

  themeToggles.forEach(btn => {
    btn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      applyTheme(newTheme);
      localStorage.setItem('aurablog-theme', newTheme);
    });
  });
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const themeIcons = document.querySelectorAll('.theme-icon');
  themeIcons.forEach(icon => {
    if (theme === 'dark') {
      icon.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>`;
    } else {
      icon.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
    }
  });
}

/* ===================================================================
   SEARCH MODAL
   =================================================================== */
function initSearchModal() {
  const searchModal = document.getElementById('searchModal');
  const openBtns = document.querySelectorAll('.open-search-modal');
  const closeBtns = document.querySelectorAll('.close-search-modal');
  const searchInput = document.getElementById('searchModalInput');

  if (!searchModal) return;

  function openModal() {
    searchModal.classList.add('open');
    setTimeout(() => searchInput?.focus(), 50);
  }

  function closeModal() {
    searchModal.classList.remove('open');
  }

  openBtns.forEach(b => b.addEventListener('click', openModal));
  closeBtns.forEach(b => b.addEventListener('click', closeModal));

  searchModal.addEventListener('click', (e) => {
    if (e.target === searchModal) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && searchModal.classList.contains('open')) {
      closeModal();
    }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      searchModal.classList.contains('open') ? closeModal() : openModal();
    }
  });
}

/* ===================================================================
   READING PROGRESS BAR
   =================================================================== */
function initReadingProgressBar() {
  const progressBar = document.getElementById('readingProgress');
  if (!progressBar) return;

  window.addEventListener('scroll', () => {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = totalHeight > 0 ? (window.scrollY / totalHeight) * 100 : 0;
    progressBar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
  });
}

/* ===================================================================
   INTERACTIVE AJAX LIKE BUTTON
   =================================================================== */
function initLikeButton() {
  const likeBtn = document.getElementById('likePostBtn');
  if (!likeBtn) return;

  likeBtn.addEventListener('click', async () => {
    const endpoint = likeBtn.dataset.endpoint;
    const csrfToken = getCookie('csrftoken');

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json'
        }
      });
      const data = await res.json();
      
      const countEl = document.getElementById('likeCount');
      if (countEl) countEl.innerText = data.likes_count;

      if (data.liked) {
        likeBtn.classList.add('liked');
        showToast('You liked this article! ❤️');
      } else {
        likeBtn.classList.remove('liked');
      }
    } catch (err) {
      console.error(err);
    }
  });
}

/* ===================================================================
   COPY LINK TO CLIPBOARD
   =================================================================== */
function initCopyLinkButtons() {
  const copyBtns = document.querySelectorAll('.btn-copy-link');
  copyBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      navigator.clipboard.writeText(window.location.href).then(() => {
        showToast('Article link copied to clipboard! 📋');
      });
    });
  });
}

/* ===================================================================
   CMS WRITING STUDIO LIVE PREVIEW & FORMATTING
   =================================================================== */
function initCmsEditorPreview() {
  const contentInput = document.getElementById('id_content');
  const previewBox = document.getElementById('cmsLivePreview');
  const wordCountEl = document.getElementById('wordCountBadge');
  const readTimeEl = document.getElementById('readTimeBadge');
  const titleInput = document.getElementById('id_title');
  const imgUrlInput = document.getElementById('id_featured_image_url');
  const imgPreview = document.getElementById('featuredImgPreview');

  if (!contentInput || !previewBox) return;

  function renderPreview() {
    const text = contentInput.value;
    const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
    const estMinutes = Math.max(1, Math.ceil(wordCount / 200));

    if (wordCountEl) wordCountEl.innerText = `${wordCount} words`;
    if (readTimeEl) readTimeEl.innerText = `${estMinutes} min read`;

    // Simple quick Markdown renderer for instant client-side preview
    let html = escapeHtml(text)
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')
      .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
      .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/gim, '<em>$1</em>')
      .replace(/`([^`]+)`/gim, '<code>$1</code>')
      .replace(/\n$/gim, '<br />')
      .replace(/\n/gim, '<br />');

    previewBox.innerHTML = html || '<p class="text-muted" style="color:var(--text-muted);font-style:italic;">Live rendered preview will appear here...</p>';
  }

  contentInput.addEventListener('input', renderPreview);
  renderPreview();

  // Quick toolbar helpers
  document.querySelectorAll('.toolbar-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const action = btn.dataset.action;
      insertFormatting(contentInput, action);
      renderPreview();
    });
  });

  // Featured Image Live Preview
  if (imgUrlInput && imgPreview) {
    imgUrlInput.addEventListener('input', () => {
      if (imgUrlInput.value) {
        imgPreview.src = imgUrlInput.value;
        imgPreview.style.display = 'block';
      }
    });
  }
}

function insertFormatting(textarea, action) {
  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;
  const selText = textarea.value.substring(start, end);
  let rep = '';

  switch (action) {
    case 'h2': rep = `\n## ${selText || 'Heading 2'}\n`; break;
    case 'h3': rep = `\n### ${selText || 'Heading 3'}\n`; break;
    case 'bold': rep = `**${selText || 'bold text'}**`; break;
    case 'italic': rep = `*${selText || 'italic text'}*`; break;
    case 'quote': rep = `\n> ${selText || 'Inspiring quote'}\n`; break;
    case 'code': rep = `\n\`\`\`\n${selText || '// code here'}\n\`\`\`\n`; break;
    case 'link': rep = `[${selText || 'link text'}](https://example.com)`; break;
    case 'list': rep = `\n- Item 1\n- Item 2\n- Item 3\n`; break;
  }

  textarea.setRangeText(rep, start, end, 'end');
  textarea.focus();
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
}

/* ===================================================================
   CMS FAST STATUS TOGGLE (Draft <-> Published)
   =================================================================== */
function initCmsStatusToggle() {
  document.querySelectorAll('.btn-toggle-status').forEach(btn => {
    btn.addEventListener('click', async () => {
      const endpoint = btn.dataset.endpoint;
      const csrfToken = getCookie('csrftoken');

      try {
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrfToken }
        });
        const data = await res.json();
        
        const badge = btn.closest('tr')?.querySelector('.badge-status');
        if (badge) {
          badge.className = `badge-status ${data.status}`;
          badge.innerText = data.status;
        }
        showToast(`Article status updated to: ${data.status}`);
      } catch (err) {
        console.error(err);
      }
    });
  });
}

/* ===================================================================
   TOAST HELPER
   =================================================================== */
function showToast(message, type = 'success') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span style="font-size: 1.1rem;">${type === 'success' ? '✓' : 'ℹ'}</span>
    <span>${message}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
