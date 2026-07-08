document.addEventListener('DOMContentLoaded', function () {
  const searchBar = document.getElementById('searchBar');
  const tableBody = document.getElementById('contributionsTableBody');

  if (searchBar && tableBody) {
    searchBar.addEventListener('input', function () {
      const query = this.value.toLowerCase();
      const rows = tableBody.querySelectorAll('tr');

      rows.forEach((row) => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
      });
    });
  }

  // Attach delete handlers
  const deleteButtons = document.querySelectorAll('.action-btn.delete');
  deleteButtons.forEach((btn) => {
    btn.addEventListener('click', function () {
      if (confirm('Delete this contribution record?')) {
        this.closest('tr').remove();
      }
    });
  });

  // Attach edit handlers
  const editButtons = document.querySelectorAll('.action-btn.edit');
  editButtons.forEach((btn) => {
    btn.addEventListener('click', function () {
      alert('Edit functionality to be implemented');
    });
  });
});
