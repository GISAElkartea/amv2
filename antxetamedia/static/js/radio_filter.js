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
  Array.forEach(shows, function(show) {
    show.setAttribute(tag, !checked);
    if (show.getAttribute('data-producer-is-hidden') === "true" &&
        show.getAttribute('data-category-is-hidden') === "true") {
      show.style.display = 'none';
    } else {
      show.style.display = 'block';
    }
  });
}

function filterShowGroups() {
  var showGroups = document.querySelectorAll('#radioShows li.radio.list');
  Array.forEach(showGroups, function(showGroup) {
    var shows = showGroup.querySelectorAll('li.show');
    var isHidden = Array.map(shows, function(show) {
      return (show.getAttribute('data-producer-is-hidden') === "true" &&
              show.getAttribute('data-category-is-hidden') === "true");
    });
    if (Array.indexOf(isHidden, false) === -1) {
      console.log("Should hide ", showGroup);
      showGroup.style.display = 'none';
    } else {
      showGroup.style.display = 'block';
    }
  });
}


var checkboxes = document.querySelectorAll('form li input');
Array.forEach(checkboxes, function(checkbox) {
  toggleLabel.apply(checkbox);
  filterShows.apply(checkbox);
  checkbox.onclick = function(event) {
    toggleLabel.apply(this);
    filterShows.apply(this);
    filterShowGroups.apply(this);
  };
});
filterShowGroups.apply();
