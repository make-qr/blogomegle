const form = document.querySelector('.comment-form');
const list = document.querySelector('.comments');
const empty = document.querySelector('.comments-empty');
const api = 'https://omeglechat.online/api/blog-notes';

function item(comment) {
  const li = document.createElement('li');
  const name = document.createElement('strong');
  const text = document.createElement('p');
  name.textContent = comment.name || 'Reader';
  text.textContent = comment.text || '';
  li.append(name, text);
  return li;
}

async function load() {
  if (!form || !list) return;
  try {
    const response = await fetch(`${api}?post=${encodeURIComponent(form.dataset.post)}`);
    const data = await response.json();
    const comments = data.comments || [];
    list.replaceChildren(...comments.map(item));
    if (empty) empty.hidden = comments.length > 0;
  } catch (_) {
    if (empty) empty.textContent = 'Comments could not be loaded.';
  }
}

if (form) {
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const status = form.querySelector('.comment-status');
    if (status) status.textContent = 'Sending…';
    const body = { post: form.dataset.post };
    new FormData(form).forEach((value, key) => { body[key] = value; });
    try {
      const response = await fetch(api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok || !data.ok) {
        if (status) status.textContent = 'That comment was not posted.';
        return;
      }
      form.reset();
      if (status) status.textContent = 'Posted.';
      load();
    } catch (_) {
      if (status) status.textContent = 'That comment was not posted.';
    }
  });
  load();
}
