import math

from django.core.urlresolvers import reverse

from . import utils

# $125 for first kid, $90 for second, $50 for third, $20 for all others
COSTS = [125, 90, 50, 20]


def get_cost(participant):
    """Return the amount owed by this parent for this session."""
    parent = participant.parent
    session = participant.session
    num_students = parent.children.filter(
        studies__klass__session=session
    ).distinct().count()
    extra = []
    if num_students > len(COSTS):
        needed = num_students - len(COSTS)
        extra = COSTS[-1:] * needed
    cost = sum(COSTS[:num_students] + extra)
    discount = None
    if 'assisting' in participant.volunteer:
        discount = 0.5
    elif 'cleaning' in participant.volunteer:
        discount = 0.2
    if discount:
        cost = math.ceil(cost * (1.0 - discount))
    return cost


def get_idhash_url(urlname, parent, session=None, **kwargs):
    reverse_kwargs = {
        'parent_id': parent.id,
        'id_hash': utils.idhash(parent.id),
    }
    if session is not None:
        reverse_kwargs['session_id'] = session.id
    reverse_kwargs.update(kwargs)

    return reverse(urlname, kwargs=reverse_kwargs)
