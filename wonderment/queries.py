# $125 for first kid, $90 for second, $50 for third, $20 for all others
COSTS = [125, 90, 50, 20]


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
