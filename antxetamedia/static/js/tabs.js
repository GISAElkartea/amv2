(function() {
  var tabs = document.querySelectorAll('.tab');

  function hideAllTabContent(tabs) {
    Array.from(tabs).forEach(function(tab) {
      tab.classList.remove('active');
    });

    var tabContents = document.querySelectorAll('.tabContent');
    Array.from(tabContents).forEach(function(content) {
      content.style.display = 'none';
    });
  }

  function showTabContent(tab) {
    tab.classList.add('active');
    contentRef = tab.getAttribute('data-tab');
    var tabContent = document.querySelector('.tabContent[data-tab="{tab}"]'.replace('{tab}', contentRef));
    tabContent.style.display = 'block';
  }

  hideAllTabContent(tabs);
  Array.from(tabs).forEach(function(tab) {
    tab.onclick = function() {
      hideAllTabContent(tabs);
      showTabContent(tab);
    };
    if (tab.classList.contains('default')) {
      showTabContent(tab);
    }
  });
})();
