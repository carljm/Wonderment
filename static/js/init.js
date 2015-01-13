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
  if (attendanceForm) {
    var parentMap = attendanceForm.data('parent-map');
    var kidLists = {};
    $("[for^='id_parents_']").each(function () {
      var label = $(this);
      var kidList = $('<ul class="children"></ul>');
      var parentId = label.find('input').attr('value');
      kidLists[parentId] = kidList;
      label.parent('li').append(kidList);
    });
    $("[for^='id_children_']").each(function () {
      var label = $(this);
      var li = label.parent('li');
      var childId = label.find('input').attr('value');
      var parentId = parentMap[childId];
      var kidList = kidLists[parentId];
      li.detach();
      kidList.append(li);
    });
  }
});
