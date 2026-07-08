const membersData = [
  {
    name: 'John Mwangi',
    phone: '0712345678',
    email: 'john@example.com',
    group: 'Group A',
    status: 'Active'
  },
  {
    name: 'Grace Njeri',
    phone: '0723456789',
    email: 'grace@example.com',
    group: 'Group B',
    status: 'Pending'
  }
];

const membersTableBody = document.getElementById('membersTableBody');
const memberModal = document.getElementById('memberModal');
const memberForm = document.getElementById('memberForm');
const modalTitle = document.getElementById('modalTitle');
const openModalBtn = document.getElementById('openMemberModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const cancelModalBtn = document.getElementById('cancelModalBtn');
const hiddenIndex = document.getElementById('memberIndex');

let editingIndex = null;

function renderMembers() {
  if (!membersTableBody) return;

  membersTableBody.innerHTML = '';

  if (membersData.length === 0) {
    membersTableBody.innerHTML = `
      <tr>
        <td colspan="6" class="empty-state">No members added yet.</td>
      </tr>
    `;
    return;
  }

  membersData.forEach((member, index) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${member.name}</td>
      <td>${member.phone}</td>
      <td>${member.email}</td>
      <td>${member.group}</td>
      <td><span class="status ${member.status.toLowerCase()}">${member.status}</span></td>
      <td>
        <button class="action-btn edit" type="button" data-index="${index}">Edit</button>
        <button class="action-btn delete" type="button" data-index="${index}">Delete</button>
      </td>
    `;
    membersTableBody.appendChild(row);
  });
}

function openModal(index = null) {
  editingIndex = index;
  memberForm.reset();
  hiddenIndex.value = '';

  if (index !== null) {
    const member = membersData[index];
    document.getElementById('memberName').value = member.name;
    document.getElementById('memberPhone').value = member.phone;
    document.getElementById('memberEmail').value = member.email;
    document.getElementById('memberGroup').value = member.group;
    document.getElementById('memberStatus').value = member.status;
    hiddenIndex.value = index;
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

function handleSubmit(event) {
  event.preventDefault();

  const member = {
    name: document.getElementById('memberName').value.trim(),
    phone: document.getElementById('memberPhone').value.trim(),
    email: document.getElementById('memberEmail').value.trim(),
    group: document.getElementById('memberGroup').value.trim(),
    status: document.getElementById('memberStatus').value
  };

  if (!member.name || !member.email || !member.group) {
    alert('Please fill in the required fields.');
    return;
  }

  if (editingIndex !== null) {
    membersData[editingIndex] = member;
  } else {
    membersData.push(member);
  }

  renderMembers();
  closeModal();
}

function handleTableClick(event) {
  const button = event.target.closest('button[data-index]');
  if (!button) return;

  const index = Number(button.getAttribute('data-index'));

  if (button.classList.contains('edit')) {
    openModal(index);
  } else if (button.classList.contains('delete')) {
    if (confirm('Delete this member?')) {
      membersData.splice(index, 1);
      renderMembers();
    }
  }
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

if (memberForm) {
  memberForm.addEventListener('submit', handleSubmit);
}

if (membersTableBody) {
  membersTableBody.addEventListener('click', handleTableClick);
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

renderMembers();
