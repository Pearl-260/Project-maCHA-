document.addEventListener('DOMContentLoaded', function () {
  const yearSpan = document.getElementById('year');
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }

  const startButton = document.querySelector('.btn-primary');
  if (startButton) {
    startButton.addEventListener('click', function (event) {
      event.preventDefault();
      document.querySelector('#about').scrollIntoView({ behavior: 'smooth' });
    });
  }
});
