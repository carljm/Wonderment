from django.db import models

from wonderment.fields import ArrayField
from wonderment.models import Parent
from .widgets import RatingWidget


ONE_TO_FIVE = [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]


class RatingField(models.IntegerField):
    def __init__(self, *a, **kw):
        self.low_desc = kw.pop('low_desc', "strongly disagree")
        self.high_desc = kw.pop('high_desc', "strongly agree")
        kw.setdefault('choices', ONE_TO_FIVE)
        kw.setdefault('blank', True)
        kw.setdefault('null', True)
        super(RatingField, self).__init__(*a, **kw)

    def formfield(self, **kwargs):
        defaults = {
            'widget': RatingWidget(
                low_desc=self.low_desc, high_desc=self.high_desc),
        }
        defaults.update(kwargs)
        return super(RatingField, self).formfield(**defaults)


class Response(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(Parent)

    hear_about = ArrayField(
        verbose_name="How did you hear about Wonderment?",
        dbtype='text',
        choices=[
            ('talking-friend', "talking with friend"),
            ('online-friend', "friend through facebook/email"),
            ('bhhe', "Black Hills Home Educators"),
            ('wonderment', "Wonderment website"),
            ('other', "Other"),
        ]
    )
    hear_about_other = models.CharField(blank=True, max_length=500)

    intention = ArrayField(
        verbose_name="My main intention in participating in Wonderment was",
        dbtype='text',
        choices=[
            ('community', "community building among families and parents"),
            (
                'socialize',
                "chance for children to socialize with other children",
            ),
            ('learning', "learning in class subject areas"),
            (
                'structure',
                (
                    "chance for children to experience more structured "
                    "group activities and instruction"
                )
            ),
            ('other', "other"),
        ]
    )
    intention_other = models.CharField(blank=True, max_length=500)

    future_participation = RatingField(
        "How likely are you to participate again in the future?",
        low_desc="definitely not",
        high_desc="very likely",
    )

    fall_mondays = RatingField(
        "Would you be likely to attend on Mondays in the fall?",
        low_desc="definitely not",
        high_desc="very likely",
    )

    for_my_kids = RatingField(
        "For my kids, Wonderment was",
        low_desc="boring/unenjoyable",
        high_desc="lots of fun!",
    )

    overall_organization = RatingField(
        "Overall, Wonderment was",
        low_desc="chaotic/confusing",
        high_desc="well organized",
    )

    overall_worthwhile = RatingField(
        "Overall, Wonderment was",
        low_desc="waste of time",
        high_desc="worthwhile",
    )

    opening_closing = RatingField(
        "For my family, the opening and closing events were",
        low_desc="waste of time",
        high_desc="worthwhile",
    )

    help_out = RatingField(
        low_desc="I was overwhelmed with my Wonderment responsibilities",
        high_desc="I would love to do more to help out",
    )

    pay_more = models.CharField(
        blank=True,
        max_length=100,
        choices=[
            (
                'pay-more',
                (
                    "I would be happy to pay more to help with "
                    "hiring qualified instructors."
                )
            ),
            (
                'good-value',
                "Wonderment pricing was a good value for our family."
            ),
            (
                'too-much',
                (
                    "We are unlikely to participate if Wonderment "
                    "registration fees increase."
                )
            ),
        ],
    )

    time_commitment = models.CharField(
        blank=True,
        max_length=100,
        choices=[
            ('once-week', "Once per week was ideal for our family."),
            ('multiple', "We would enjoy attending multiple times per week."),
            ('too-much', "Once per week was too frequent for us."),
        ],
    )

    timing_comments = models.TextField(
        "Comments on time of day, day of week, length of classes or session",
        blank=True,
    )

    class_subjects_art = RatingField(
        "The Art subject was",
        low_desc="not valuable",
        high_desc="valuable",
    )

    class_subjects_spanish = RatingField(
        "The Spanish subject was",
        low_desc="not valuable",
        high_desc="valuable",
    )

    class_subjects_dance = RatingField(
        "The Dance subject was",
        low_desc="not valuable",
        high_desc="valuable",
    )

    class_subjects_freeplay = RatingField(
        "The free play time was",
        low_desc="not valuable",
        high_desc="valuable",
    )

    future_classes = models.TextField(
        (
            "Classes or activities I would like "
            "to see Wonderment offer in the future"
        ),
        blank=True,
    )

    teachers_barbara = RatingField(
        "Barbara Linares (5-7 Art, 7-14 Spanish)",
        low_desc="not much learned",
        high_desc="provided valuable learning experiences",
    )

    teachers_shawnda = RatingField(
        "Shawnda Ruml (18mo - 4yr Art)",
        low_desc="not much learned",
        high_desc="provided valuable learning experiences",
    )

    teachers_sharon = RatingField(
        "Sharon Grey (8 - 14 Drawing)",
        low_desc="not much learned",
        high_desc="provided valuable learning experiences",
    )

    teachers_karissa = RatingField(
        "Karissa Loewen (18mo - 7yr Spanish)",
        low_desc="not much learned",
        high_desc="provided valuable learning experiences",
    )

    most_valuable = models.TextField(
        (
            "The most valuable or interesting class, outcome or activity "
            "in Wonderment for my family was"
        ),
        blank=True,
    )

    suggestions = models.TextField("Suggestions for improvement", blank=True)

    other_dreams = models.TextField(
        (
            "Any other comments/suggestions/ideas/dreams "
            "for the future of Wonderment"
        ),
        blank=True,
    )
