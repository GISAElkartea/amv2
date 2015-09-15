(function() {
  function hideAllTabContent() {
    var tabContents = document.querySelectorAll('.tabContent');
    Array.forEach(tabContents, function(content) {
      content.style.display = 'none';
    });
  }

  function showTabContent() {
    var tab = this.getAttribute('data-tab');
    var tabContent = document.querySelector('.tabContent[data-tab="{tab}"]'.replace('{tab}', tab));
    tabContent.style.display = 'block';
  }

  hideAllTabContent();
  var tabs = document.querySelectorAll('.tab');
  Array.forEach(tabs, function(tab) {
    tab.onclick = function() {
      hideAllTabContent();
      showTabContent.apply(tab);
    };
    if (tab.classList.contains('default')) {
      showTabContent.apply(tab);
    }
  });
})();
