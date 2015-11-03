jQuery(function($) {
  $('.formlist').superformset({
    prefix: 'children',
    containerSel: '.container',
    addTriggerSel: '.add-child',
  });
  $('.formlist').on('click', '.remove-child', function (e) {
    var form = $(this).closest('.dynamic-form').animate({
      height: 'toggle', opacity: 'toggle'}, function () {
        if (form.hasClass('new-row')) { form.remove(); }
      });
    form.find("[id$='-DELETE']").prop('checked', true);
    e.preventDefault();
  });

  var attendanceForm = $('#attendance-form');
  if (attendanceForm.length) {
    var parentRadioSel = '.parent-attendance-form input[type="radio"]';
    attendanceForm.on('change', parentRadioSel, function () {
      var newVal = $(this).val();
      var parentId = $(this).closest(
        '.parent-attendance-form').data('parent-id');
      attendanceForm.find(
        '.child-attendance-form[data-parent-id="' + parentId + '"] ' +
          'input[type="radio"]'
      ).filter(function () {
        return $(this).val() === '' && $(this).prop('checked');
      }).each(function () {
        var inputName = $(this).attr('name');
        attendanceForm.find('input[name="' + inputName + '"]').val([newVal]);
      });
    });
  }

  var surveyForm = $('.evaluation-form');
  if (surveyForm.length) {
    var initOtherField = function (fieldName) {
      var checkboxGroup = $('input[name="' + fieldName + '"]');
      var checkbox = checkboxGroup.filter('[value="other"]');
      var otherInputGroup = $('#id_' + fieldName + '_other').parent();
      var update = function () {
        if (checkbox.prop('checked')) {
          otherInputGroup.show();
        } else {
          otherInputGroup.hide();
        }
      };
      update();
      checkboxGroup.on('change', update);
    };
    initOtherField('hear_about');
    initOtherField('intention');
  }

  var regForm = $('#participant-form');
  if (regForm.length) {
    var initDependentField = function (checkboxName, dependentName) {
      var checkbox = $('input[name="' + checkboxName + '"]');
      var dependent = $('#id_' + dependentName).parent();
      var update = function () {
        if (checkbox.prop('checked')) {
          dependent.show();
        } else {
          dependent.hide();
        }
      };
      update();
      checkbox.on('change', update);
    };
    initDependentField('drop_off', 'pick_up_names');
  }
});
