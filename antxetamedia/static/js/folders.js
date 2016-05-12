(function() {
  function toggleFold(event) {
    var content = this.querySelector('.folderContent');
    content.style.display = window.getComputedStyle(content).display !== 'none' ? 'none' : 'block';
  }

  var folders = document.querySelectorAll('.folder');
  Array.from(folders).forEach(function(folder) {
      folder.onclick = toggleFold;
  });
})();
