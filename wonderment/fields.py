import floppyforms.__future__ as forms
from django.contrib.postgres import fields
from djorm_pgarray import fields as djorm_fields


class ArrayChoiceField(fields.ArrayField):
    """An ArrayField that uses a multi-choice form field if choices are set."""
    def formfield(self, **kwargs):
        defaults = {}
        if self.base_field.choices:
            defaults = {
                'form_class': forms.TypedMultipleChoiceField,
                'coerce': self.base_field.to_python,
                'choices': self.base_field.choices,
                'widget': forms.CheckboxSelectMultiple,
            }
            defaults.update(kwargs)
            # skip the parent formfield method; it adds base_field, which
            # TypedMultipleChoiceField chokes on
            return super(fields.ArrayField, self).formfield(**defaults)
        return super(ArrayChoiceField, self).formfield(**kwargs)


class ArrayField(djorm_fields.ArrayField):
    """An ArrayField that returns an empty list instead of None.

    DEPRECATED: use contrib.postgres ArrayField instead.
    """
    def to_python(self, value):
        """Return empty list instead of None."""
        return super(ArrayField, self).to_python(value) or []
