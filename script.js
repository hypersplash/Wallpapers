let currentFiles = [];

function loadWallpapers(folder) {
  fetch(`./${folder}/wallpapers.json`)
    .then(r => r.json())
    .then(files => {
      currentFiles = files;
      renderGallery(folder, files);
    });
}

function renderGallery(folder, files) {
  const gallery = document.getElementById('gallery');
  gallery.innerHTML = files.map(file => `
    <div class="gallery-item">
      <img src="./${folder}/${file}" alt="${file}" loading="lazy">
      <p>${file}</p>
      <div class="btns">
        <button onclick="downloadImage('./${folder}/${file}')">⬇️</button>
        <button onclick="copyImageLink('./${folder}/${file}')">🔗</button>
      </div>
    </div>
  `).join('');
}

function searchImages(input) {
  const query = input.value.toLowerCase();
  const filtered = currentFiles.filter(f => f.toLowerCase().includes(query));
  renderGallery(getCurrentFolder(), filtered);
}

function sortImages() {
  currentFiles.reverse();
  renderGallery(getCurrentFolder(), currentFiles);
}

function toggleTheme() {
  document.body.classList.toggle('light');
  localStorage.setItem('theme', document.body.classList.contains('light') ? 'light' : 'dark');
}

function downloadImage(url) {
  const a = document.createElement('a');
  a.href = url;
  a.download = url.split('/').pop();
  a.click();
}

function copyImageLink(url) {
  navigator.clipboard.writeText(window.location.origin + '/' + url);
  alert('Copied: ' + url);
}

function getCurrentFolder() {
  return window.location.pathname.includes('phone') ? 'Phone' : 'Computer';
}

// restore theme on load
window.addEventListener('DOMContentLoaded', () => {
  if (localStorage.getItem('theme') === 'light') document.body.classList.add('light');
});
