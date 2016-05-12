(function() {
  function hideAllTabContent() {
    var tabs = document.querySelectorAll('.tab');
    Array.from(tabs).forEach(function(tab) {
      tab.classList.remove('active');
    });

    var tabContents = document.querySelectorAll('.tabContent');
    Array.from(tabContents).forEach(function(content) {
      content.style.display = 'none';
    });
  }

  function showTabContent() {
    this.classList.add('active');
    var tab = this.getAttribute('data-tab');
    var tabContent = document.querySelector('.tabContent[data-tab="{tab}"]'.replace('{tab}', tab));
    tabContent.style.display = 'block';
  }

  hideAllTabContent();
  var tabs = document.querySelectorAll('.tab');
  Array.from(tabs).forEach(function(tab) {
    tab.onclick = function() {
      hideAllTabContent();
      showTabContent.apply(tab);
    };
    if (tab.classList.contains('default')) {
      showTabContent.apply(tab);
    }
  });
})();
