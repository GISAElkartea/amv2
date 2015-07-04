function toggleLabel(event) {
  this.parentElement.classList.toggle('checked', this.checked);
}

var checkboxes = document.querySelectorAll('form li input');
Array.forEach(checkboxes, function(checkbox) {
  toggleLabel.apply(checkbox);
  checkbox.onclick = toggleLabel;
});
