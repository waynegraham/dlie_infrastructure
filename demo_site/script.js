let resources = [];
let currentFilter = 'all';
let currentPage = 1;
const pageSize = 20;
let totalPages = 1;

// Fetch paginated resources from API
async function fetchResources(page = 1) {
  try {
    const url = `http://localhost:8000/resources?page=${page}&page_size=${pageSize}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Network response was not ok');
    const data = await response.json();
    resources = data.items;
    totalPages = Math.ceil(data.total / data.page_size);
    currentPage = data.page;
    updatePagination();
    applyFilters();
  } catch (err) {
    const container = document.getElementById('results');
    container.innerHTML = `<p class="error">Error loading resources: ${err.message}</p>`;
  }
}

function displayResources(list) {
  const container = document.getElementById('results');
  container.innerHTML = '';
  if (!list.length) {
    container.innerHTML = '<p>No resources found.</p>';
    return;
  }

  list.forEach(r => {
    const card = document.createElement('div');
    card.className = 'card';

    const title = document.createElement('h2');
    title.textContent = r.title;
    card.appendChild(title);

    const type = document.createElement('div');
    type.className = 'type';
    type.textContent = r.type;
    card.appendChild(type);

    const provider = document.createElement('div');
    provider.className = 'provider';
    provider.textContent = r.provider;
    card.appendChild(provider);

    const date = document.createElement('div');
    date.className = 'date';
    date.textContent = new Date(r.date).toLocaleDateString();
    card.appendChild(date);

    const abstract = document.createElement('p');
    abstract.className = 'abstract';
    abstract.textContent = r.abstract || '';
    card.appendChild(abstract);

    const link = document.createElement('a');
    link.href = r.url;
    link.textContent = 'View Resource';
    link.target = '_blank';
    card.appendChild(link);

    container.appendChild(card);
  });
}

function updatePagination() {
  document.getElementById('pageInfo').textContent = `Page ${currentPage} of ${totalPages}`;
  document.getElementById('prevBtn').disabled = currentPage <= 1;
  document.getElementById('nextBtn').disabled = currentPage >= totalPages;
}

function setupPagination() {
  document.getElementById('prevBtn').addEventListener('click', () => {
    if (currentPage > 1) fetchResources(currentPage - 1);
  });
  document.getElementById('nextBtn').addEventListener('click', () => {
    if (currentPage < totalPages) fetchResources(currentPage + 1);
  });
}

function applyFilters() {
  let filtered = resources.filter(r => r.title.toLowerCase().includes(document.getElementById('searchBox').value.toLowerCase()));
  if (currentFilter !== 'all') {
    filtered = filtered.filter(r => r.type === currentFilter);
  }
  displayResources(filtered);
}

function setFilter(type) {
  currentFilter = type;
  document.querySelectorAll('.filters button').forEach(btn => btn.classList.toggle('active', btn.dataset.type === type));
  applyFilters();
}

function onSearch() {
  applyFilters();
}

// Initialization
window.onload = () => { setupPagination(); fetchResources(1); };