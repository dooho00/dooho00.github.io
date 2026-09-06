document.querySelectorAll('[data-dialog]').forEach((button) => {
  button.addEventListener('click', () => {
    document.getElementById(button.dataset.dialog).showModal();
    document.body.classList.add('dialog-open');
  });
});

document.querySelectorAll('.info-dialog').forEach((dialog) => {
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    const bounds = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right ||
        event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
  });
  dialog.addEventListener('close', () => document.body.classList.remove('dialog-open'));
});
