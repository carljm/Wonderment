from . import models


# $135 for first kid, $95 for second, $55 for third, $25 for all others
COSTS = [135, 95, 55, 25]


def get_cost(parent, session):
    """Return the amount owed by this parent for this session."""
    num_students = parent.children.filter(
        studies__klass__session=session
    ).distinct().count()
    extra = []
    if num_students > len(COSTS):
        needed = num_students - len(COSTS)
        extra = COSTS[-1:] * needed
    return sum(COSTS[:num_students] + extra)
