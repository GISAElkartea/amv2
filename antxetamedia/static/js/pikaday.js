(function() {
  var i18n = {
    previousMonth : gettext('Previous Month'),
    nextMonth     : gettext('Next Month'),
    months        : [
      gettext('January'),
      gettext('February'),
      gettext('March'),
      gettext('April'),
      gettext('May'),
      gettext('June'),
      gettext('July'),
      gettext('August'),
      gettext('September'),
      gettext('October'),
      gettext('November'),
      gettext('December')
    ],
    weekdays      : [
      gettext('Sunday'),
      gettext('Monday'),
      gettext('Tuesday'),
      gettext('Wednesday'),
      gettext('Thursday'),
      gettext('Friday'),
      gettext('Saturday')
    ],
    weekdaysShort : [
      gettext('Sun'),
      gettext('Mon'),
      gettext('Tue'),
      gettext('Wed'),
      gettext('Thu'),
      gettext('Fri'),
      gettext('Sat')
    ]
  };

  var inputBoxes = document.querySelectorAll('input.pikaday');
  Array.from(inputBoxes).forEach(function(inputBox) {
    new Pikaday({
      field: inputBox,
      format: 'YYYY-MM-DD',
      i18n: i18n
    });
  });
})();
