var inputBoxes = document.querySelectorAll('input.pikaday');
Array.forEach(inputBoxes, function(inputBox) {
  new Pikaday({
    field: inputBox,
    format: 'YYYY-MM-DD'
  });
});
