jQuery(function($) {
  $('#participant-form .formlist').superformset({
    prefix: 'children',
    containerSel: '.container',
    addTriggerSel: '.add-child',
  });
  $('#participant-form .formlist').on('click', '.remove-child', function (e) {
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

  var classSelectForm = $('#select-classes-form');
  if (classSelectForm.length) {
    // shim Date.now() for IE8 and earlier
    if (!Date.now) {
      Date.now = function() { return new Date().getTime(); }
    }
    var classInputs = classSelectForm.find('.class-item-input');
    var updateWaitlist = function () {
      var numStudentsByClassId = {};
      var lastCheckedByWhenId = {};
      classInputs.sort(function (a, b) {
        var $a = $(a);
        var $b = $(b);
        var aChecked = $a.prop('checked');
        var bChecked = $b.prop('checked');
        var aLastChecked = $a.data('last-checked');
        var bLastChecked = $b.data('last-checked');
        if (!aChecked || !aLastChecked) { return 1; }
        if (!bChecked || !bLastChecked) { return -1; }
        return aLastChecked - bLastChecked;
      }).each(function () {
        var aClass = $(this);
        var whenField = aClass.closest('.panel-body').find('[name$="-when"]');
        var whenFieldId = whenField.attr('id');
        var value = aClass.attr('value');
        var lastChecked = aClass.data('last-checked');
        var label = aClass.closest('label');
        var classId = aClass.data('class-id');
        var numStudents = numStudentsByClassId[classId] || 0;
        var maxStudents = aClass.data('max-students');
        var lastCheckedByValue = lastCheckedByWhenId[whenFieldId] || {};
        if (aClass.prop('checked') && lastChecked) {
          lastCheckedByValue[value] = lastChecked;
        }
        lastCheckedByWhenId[whenFieldId] = lastCheckedByValue;
        if (numStudents >= maxStudents) {
          aClass.addClass('waitlist');
          label.addClass('waitlist');
        } else {
          if (aClass.hasClass('waitlist-dupe')) {
            aClass.removeClass('waitlist-dupe');
            var aDay = aClass.data('weekday');
            var conflictingClasses = aClass.closest('ul').find(
              '.class-item-input[data-weekday="' + aDay + '"]'
            ).not(aClass).not('waitlist');
            conflictingClasses.each(function () {
              $(this).prop('checked', false);
            });
          }
          aClass.removeClass('waitlist');
          label.removeClass('waitlist');
        }
        if (aClass.prop('checked')) {
          numStudentsByClassId[classId] = numStudents + 1;
        }
      });
      $.each(lastCheckedByWhenId, function (whenId, byVal) {
        var hiddenInput = classSelectForm.find('#' + whenId);
        hiddenInput.val(JSON.stringify(byVal));
      });
    }
    updateWaitlist();
    classInputs.on('change', function () {
      var thisClass = $(this);
      if (thisClass.prop('checked')) {
        thisClass.data('last-checked', Date.now());
        var thisDay = thisClass.data('weekday');
        var thisStart = thisClass.data('start');
        var thisEnd = thisClass.data('end');
        var sameDayClasses = thisClass.closest('ul').find(
          '.class-item-input[data-weekday="' + thisDay + '"]'
        ).not(thisClass);
        sameDayClasses.each(function () {
          var aClass = $(this);
          var aStart = aClass.data('start');
          var aEnd = aClass.data('end');
          if (aClass.prop('checked') && (aEnd > thisStart) && (aStart < thisEnd)) {
            var thisWait = thisClass.hasClass('waitlist');
            var aWait = aClass.hasClass('waitlist');
            if (thisWait) {
              thisClass.addClass('waitlist-dupe');
            }
            if (aWait) {
              aClass.addClass('waitlist-dupe');
            }
            if (!thisWait && !aWait) {
              aClass.prop('checked', false);
              aClass.removeClass('waitlist-dupe');
            }
          }
        });
      } else {
        thisClass.removeClass('waitlist-dupe');
      }
      updateWaitlist();
    });
  }
});
