const resources = [
  { title: 'Ecology and Society', type: 'Journal', url: 'https://www.ecologyandsociety.org' },
  { title: 'Global Biodiversity Information Facility', type: 'Dataset', url: 'https://www.gbif.org' },
  { title: 'The Sustainability Agenda', type: 'Podcast', url: 'https://www.thesustainabilityagenda.com' },
  // Add more resources here
];
let currentFilter = 'all';

function displayResources(list) {
  const container = document.getElementById('results');
  container.innerHTML = '';
  if (list.length === 0) {
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

    const link = document.createElement('a');
    link.href = r.url;
    link.textContent = 'View Resource';
    link.target = '_blank';
    card.appendChild(link);

    container.appendChild(card);
  });
}

function filterResources() {
  const query = document.getElementById('searchBox').value.toLowerCase();
  let filtered = resources.filter(r => r.title.toLowerCase().includes(query));
  if (currentFilter !== 'all') {
    filtered = filtered.filter(r => r.type === currentFilter);
  }
  displayResources(filtered);
}

function setFilter(type) {
  currentFilter = type;
  document.querySelectorAll('.filters button').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.type === type);
  });
  filterResources();
}

// Initial load
window.onload = () => displayResources(resources);
