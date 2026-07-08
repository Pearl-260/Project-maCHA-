function confirmLogout(event) {
  event.preventDefault();
  
  if (confirm('Are you sure you want to log out?')) {
    // Redirect to logout route
    window.location.href = event.currentTarget.href;
  }
}

// Attach logout handler to all logout links when page loads
document.addEventListener('DOMContentLoaded', function() {
  const logoutLinks = document.querySelectorAll('a[href*="/logout"]');
  logoutLinks.forEach(link => {
    link.addEventListener('click', confirmLogout);
  });
});
