from djorm_pgarray import fields


class ArrayField(fields.ArrayField):
    """An ArrayField that returns an empty list instead of None.

    DEPRECATED: use contrib.postgres ArrayField instead.
    """
    def to_python(self, value):
        """Return empty list instead of None."""
        return super(ArrayField, self).to_python(value) or []
