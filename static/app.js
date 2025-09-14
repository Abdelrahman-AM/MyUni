// Simple client-side favorites management and save flow
(function () {
  const storeKey = 'myuni:favorites';
  const cityKey = 'myuni:city';

  function getFavs() {
    try { return JSON.parse(localStorage.getItem(storeKey) || '[]'); } catch { return []; }
  }
  function setFavs(list) {
    localStorage.setItem(storeKey, JSON.stringify(list));
    renderFavBadges();
  }
  function toggleFav(slug) {
    const list = new Set(getFavs());
    if (list.has(slug)) list.delete(slug); else list.add(slug);
    setFavs(Array.from(list));
    updateCardButtons();
  }
  function getCity() {
    return localStorage.getItem(cityKey) || '';
  }
  function setCity(city) {
    localStorage.setItem(cityKey, city || '');
    const badge = document.getElementById('selectedCity');
    if (badge) badge.textContent = city || 'None';
    const btn = document.getElementById('cityDropdownBtn');
    if (btn && city) btn.textContent = city;
  }

  // Expose for templates
  window.MyUni = {
    changeCity: function(city) { setCity(city); },
    browseUniversities: function() {
      const city = getCity();
      if (!city) { alert('Please select a city first!'); return; }
      window.location.href = `/universities?city=${encodeURIComponent(city)}`;
    },
    toggleFavorite: toggleFav,
    getFavorites: getFavs,
    saveList: async function(name, email, note) {
      const payload = { name, email, note, city: getCity(), favorites: getFavs() };
      const res = await fetch('/api/save', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error('Failed to save');
      return res.json();
    }
  };

  function updateCardButtons() {
    const favs = new Set(getFavs());
    document.querySelectorAll('[data-fav-btn]')
      .forEach(btn => {
        const slug = btn.getAttribute('data-slug');
        const active = favs.has(slug);
        btn.classList.toggle('btn-outline-danger', !active);
        btn.classList.toggle('btn-danger', active);
        btn.innerHTML = active ? '♥ Saved' : '♡ Save';
      });
  }

  function renderFavBadges() {
    const countEls = document.querySelectorAll('[data-fav-count]');
    const n = getFavs().length;
    countEls.forEach(el => el.textContent = n);
  }

  document.addEventListener('DOMContentLoaded', () => {
    // Initialize city badge if present
    const c = getCity();
    if (c) setCity(c);
    renderFavBadges();
    updateCardButtons();
    // Reveal on scroll
    try {
      const els = document.querySelectorAll('.reveal');
      if ('IntersectionObserver' in window && els.length) {
        const io = new IntersectionObserver((entries)=>{
          entries.forEach(e=>{
            if (e.isIntersecting) {
              e.target.classList.add('in-view');
              io.unobserve(e.target);
            }
          })
        }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
        els.forEach(el => io.observe(el));
      } else {
        els.forEach(el => el.classList.add('in-view'));
      }
    } catch {}
  });
})();
