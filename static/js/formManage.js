function addForm() {
  $('#electForm div.fieldWrapper').formset({
      prefix: '{{ formset.prefix }}',
  });
}
