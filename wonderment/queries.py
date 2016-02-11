from . import models


BASE_COST = 125
EXTRA_DAY_DISCOUNT = 10
EXTRA_KID_DISCOUNT = 15
# This means that there's no additional discount for fifth, sixth, etc kids,
# they all pay the fourth-kid rate.
MAX_DISCOUNTED_KIDS = 4
FREE_AFTER = 2  # All kids after the second are free


def get_cost(parent, session):
    """Return the amount owed by this parent for this session."""
    students = models.Student.objects.filter(
        child__in=parent.children.all(), klass__session=session
    ).select_related('klass')
    weekdays_by_child_id = {}
    for student in students:
        weekdays_by_child_id.setdefault(student.child_id, set()).add(
            student.klass.weekday)
    day_counts = {}
    for weekday_set in weekdays_by_child_id.values():
        num_days = len(weekday_set)
        for i in range(num_days):
            day_counts[i + 1] = day_counts.get(i + 1, 0) + 1
    cost = 0
    for num_days, kid_count in day_counts.items():
        kid_count = min(kid_count, FREE_AFTER)
        base_cost = BASE_COST - (EXTRA_DAY_DISCOUNT * (num_days - 1))
        dkids = min(kid_count, MAX_DISCOUNTED_KIDS)
        kid_discount = (
            EXTRA_KID_DISCOUNT * ((dkids * (dkids - 1)) / 2))
        kid_discount += (
            EXTRA_KID_DISCOUNT *
            (MAX_DISCOUNTED_KIDS - 1) *
            (kid_count - dkids)
        )
        day_cost = (base_cost * kid_count) - kid_discount
        cost += day_cost
    return int(cost)
