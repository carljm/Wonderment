jQuery(function($) {
  $('.formlist').superformset({
    prefix: 'children',
    containerSel: '.container',
    addTriggerSel: '.add-child',
  });
  $("").hide();
  $('.formlist').on('click', '.remove-child', function (e) {
    var form = $(this).closest('.dynamic-form').animate({
      height: 'toggle', opacity: 'toggle'}, function () {
        if (form.hasClass('new-row')) { form.remove(); }
      });
    form.find("[id$='-DELETE']").prop('checked', true);
    e.preventDefault();
  });
});
