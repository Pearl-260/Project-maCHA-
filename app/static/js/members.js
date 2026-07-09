const membersTableBody = document.getElementById('membersTableBody');
const memberModal = document.getElementById('memberModal');
const memberForm = document.getElementById('memberForm');
const modalTitle = document.getElementById('modalTitle');
const openModalBtn = document.getElementById('openMemberModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const cancelModalBtn = document.getElementById('cancelModalBtn');
const hiddenIndex = document.getElementById('memberIndex');

let editingIndex = null;

function openModal(index = null) {
  editingIndex = index;
  memberForm.reset();
  hiddenIndex.value = '';

  if (index !== null) {
    modalTitle.textContent = 'Edit Member';
  } else {
    modalTitle.textContent = 'Add Member';
  }

  memberModal.classList.add('open');
}

function closeModal() {
  memberModal.classList.remove('open');
  memberForm.reset();
  hiddenIndex.value = '';
  editingIndex = null;
}

if (openModalBtn) {
  openModalBtn.addEventListener('click', () => openModal(null));
}

if (closeModalBtn) {
  closeModalBtn.addEventListener('click', closeModal);
}

if (cancelModalBtn) {
  cancelModalBtn.addEventListener('click', closeModal);
}

if (memberModal) {
  memberModal.addEventListener('click', (event) => {
    if (event.target === memberModal) {
      closeModal();
    }
  });
}

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && memberModal && memberModal.classList.contains('open')) {
    closeModal();
  }
});
