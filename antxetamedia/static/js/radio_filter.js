(function() {
  function toggleLabel() {
    this.parentElement.classList.toggle('checked', this.checked);
  }

  function filterShows() {
    var filter = this.name,
        value = this.value,
        checked = this.checked;
    var selector = '#radioShows li.show[data-{filter}="{value}"]',
        tag = 'data-{filter}-is-hidden';
    selector = selector.replace('{filter}', filter);
    selector = selector.replace('{value}', value);
    tag = tag.replace('{filter}', filter);
    var shows = document.querySelectorAll(selector);
    console.log(selector);
    Array.from(shows).forEach(function(show) {
      show.setAttribute(tag, !checked);
      if (show.getAttribute('data-producer-is-hidden') === "true" ||
          show.getAttribute('data-category-is-hidden') === "true") {
        show.style.display = 'none';
      } else {
        show.style.display = 'block';
      }
    });
  }

  var checkboxes = document.querySelectorAll('form li input');
  Array.from(checkboxes).forEach(function(checkbox) {
    toggleLabel.apply(checkbox);
    filterShows.apply(checkbox);
    checkbox.onclick = function(event) {
      toggleLabel.apply(this);
      filterShows.apply(this);
    };
  });
})();
