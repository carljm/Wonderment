from djorm_pgarray import fields


class ArrayField(fields.ArrayField):
    """An ArrayField that returns an empty list instead of None."""
    def to_python(self, value):
        """Return empty list instead of None."""
        return super(ArrayField, self).to_python(value) or []
