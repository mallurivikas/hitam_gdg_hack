// Component Loader - Loads header and footer into pages
async function loadComponent(componentName, targetId) {
  try {
    const response = await fetch(`components/${componentName}.html`);
    const html = await response.text();
    document.getElementById(targetId).innerHTML = html;
  } catch (error) {
    console.error(`Error loading ${componentName}:`, error);
  }
}

// Load header and footer when page loads
document.addEventListener('DOMContentLoaded', async function() {
  await loadComponent('header', 'header-placeholder');
  await loadComponent('footer', 'footer-placeholder');
  
  // Re-highlight navigation after header loads
  highlightActiveNav();
  
  // Re-attach mobile menu listener after header loads
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', toggleMobileMenu);
  }
  
  // Close mobile menu on link click
  const mobileNavLinks = document.querySelectorAll('#mobile-menu .nav-link');
  mobileNavLinks.forEach(link => {
    link.addEventListener('click', closeMobileMenu);
  });
});
