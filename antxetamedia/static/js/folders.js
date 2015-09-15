(function() {
  function toggleFold(event) {
    var content = this.querySelector('.folderContent');
    content.style.display = window.getComputedStyle(content).display !== 'none' ? 'none' : 'block';
  }

  var folders = document.querySelectorAll('.folder');
  Array.forEach(folders, function(folder) {
      folder.onclick = toggleFold;
  });
})();
