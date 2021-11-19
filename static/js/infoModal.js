var exampleModal = document.getElementById('modalTask');


exampleModal.addEventListener('show.bs.modal', function (event) {

  var button = event.relatedTarget

  var recipient = button.getAttribute('data-bs-whatever')
  var recipientId = button.getAttribute('data-task_id')


  var modalTitle = exampleModal.querySelector('.modal-title')
  var taskName = document.getElementById('taskName')
  var taskId = document.getElementById('taskId')
  

  modalTitle.textContent = 'Edit task ' + recipient
  taskName.value = recipient
  taskId.value = recipientId
})
