// ===== NAVBAR SCROLL =====
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 50);
});

// ===== HAMBURGER MENU =====
const hamburger = document.getElementById('hamburger');
const navLinks = document.querySelector('.nav-links');
hamburger?.addEventListener('click', () => navLinks.classList.toggle('open'));

// ===== SCROLL REVEAL =====
const revealEls = document.querySelectorAll('.service-card, .doctor-card, .info-item');
revealEls.forEach(el => el.classList.add('reveal'));

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), i * 80);
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });
revealEls.forEach(el => observer.observe(el));

// ===== CONTACT FORM (AJAX) =====
const form = document.getElementById('contactForm');
const formMsg = document.getElementById('formMsg');

form?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = form.querySelector('button[type=submit]');
  btn.textContent = 'Sending...'; btn.disabled = true;

  const data = new FormData(form);

  try {
    const res = await fetch('/api/contact/', {
      method: 'POST',
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
      body: data
    });
    const json = await res.json();
    if (res.ok && json.success) {
      formMsg.className = 'form-msg success';
      formMsg.textContent = '✅ Appointment request sent! We will call you shortly.';
      form.reset();
    } else {
      throw new Error(json.error || 'Server error');
    }
  } catch (err) {
    formMsg.className = 'form-msg error';
    formMsg.textContent = '❌ ' + err.message;
  } finally {
    btn.textContent = 'Send Appointment Request →'; btn.disabled = false;
  }
});

// ===== LOAD DOCTORS FROM API =====
async function loadDoctors() {
  try {
    const res = await fetch('/api/doctors/');
    const doctors = await res.json();
    if (!doctors.length) return;
    const grid = document.getElementById('doctorsGrid');
    const colors = [
      'linear-gradient(135deg,#FF6B6B,#FF8E53)',
      'linear-gradient(135deg,#4ECDC4,#44A3AA)',
      'linear-gradient(135deg,#A29BFE,#6C5CE7)',
      'linear-gradient(135deg,#FD79A8,#E84393)',
      'linear-gradient(135deg,#FFE66D,#FDCB6E)',
    ];
    grid.innerHTML = doctors.map((doc, i) => `
      <div class="doctor-card reveal">
        <div class="doc-avatar" style="background:${colors[i % colors.length]}">
          ${doc.name.split(' ').map(n=>n[0]).join('').slice(0,2)}
        </div>
        <h4>${doc.name}</h4>
        <span class="spec">${doc.specialization}</span>
        <p>⭐ ${doc.rating} &nbsp;|&nbsp; ${doc.experience} yrs exp.</p>
        <a href="#contact" class="btn-small">Book Now</a>
      </div>
    `).join('');
    // Re-observe new cards
    grid.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  } catch {}
}
loadDoctors();

// ===== CSRF COOKIE HELPER =====
function getCookie(name) {
  const v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
  return v ? v[2] : null;
}

// ===== SMOOTH ACTIVE NAV =====
const sections = document.querySelectorAll('section[id]');
const links = document.querySelectorAll('.nav-links a');
window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(s => { if (window.scrollY >= s.offsetTop - 120) current = s.id; });
  links.forEach(a => {
    a.style.color = a.getAttribute('href') === '#'+current ? 'var(--primary)' : '';
  });
});