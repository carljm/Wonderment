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
    parent = models.ForeignKey(Parent, related_name='fall2015eval')

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
            (
                'break',
                (
                    "something I could feel good about my kids "
                    "participating in while I had a needed break"
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

    days = ArrayField(
        verbose_name="Which days would work for you for next session?",
        dbtype="text",
        choices=[
            ('mon', "Monday"),
            ('tue', "Tuesday"),
            ('wed', "Wednesday"),
            ('thu', "Thursday"),
            ('fri', "Friday"),
            ('sat', "Saturday"),
            ('sun', "Sunday"),
        ],
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

    help_out = models.TextField(
        verbose_name=(
            "Comments on your experience as an assistant, "
            "and/or on your child's experience "
            "of the assistants in the classroom:"
        ),
        blank=True,
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
        (
            "Comments on time of day, day of week, "
            "length of classes or session, cost"
        ),
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

    class_subjects_improv = RatingField(
        "The Improvisation class was",
        low_desc="not valuable",
        high_desc="valuable",
    )

    class_subjects_film = RatingField(
        "The Film-making class was",
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

    teachers_dominique = RatingField(
        "Dominique Beck (Toddlers 18mo-3yr)",
        low_desc="not much learned",
        high_desc="provided valuable learning experiences",
    )

    teachers_lisa = RatingField(
        "Ms. Lisa (Dance 18mo-7yr)",
        low_desc="not much learned",
        high_desc="provided valuable learning experiences",
    )

    teachers_rachel = RatingField(
        "Rachel Ballast (Spanish 3-11yr)",
        low_desc="not much learned",
        high_desc="provided valuable learning experiences",
    )

    teachers_trevor = RatingField(
        "Trevor Kasma (Improvisation 8-11yr)",
        low_desc="not much learned",
        high_desc="provided valuable learning experiences",
    )

    teachers_kema = RatingField(
        "Kema Teamer (Artistic Team Building, 3-11yr)",
        low_desc="not much learned",
        high_desc="provided valuable learning experiences",
    )

    teachers_luke = RatingField(
        "Luke Anderson (Film-making 12+ yr)",
        low_desc="not much learned",
        high_desc="provided valuable learning experiences",
    )

    teacher_comments = models.TextField(
        "Any comments on teachers or assistants",
        blank=True,
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

    def __str__(self):
        return self.parent.name


class TeacherResponse(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    teacher_name = models.CharField(max_length=254)

    communication = RatingField(
        "Expectations, policies, dates, times, and information needed were",
        low_desc="unclear",
        high_desc="clear",
    )

    communication_comments = models.TextField(
        "Other comments on communication from Wonderment:",
        blank=True,
    )

    location = RatingField(
        (
            "The classroom space available was conducive to an effective "
            "and safe learning environment."
        ),
        low_desc="disagree",
        high_desc="agree",
    )

    location_comments = models.TextField(
        "Other comments on location and facilities:",
        blank=True,
    )

    again = RatingField(
        "I would consider teaching again with Wonderment.",
        low_desc="disagree",
        high_desc="agree",
    )

    again_comments = models.TextField(
        "Comments about teaching again:",
        blank=True,
    )

    compensation = RatingField(
        "Compensation was clear, timely, and reasonable.",
        low_desc="agree",
        high_desc="disagree",
    )

    compensation_comments = models.TextField(
        "Comments about compensation:",
        blank=True,
    )

    assistant = RatingField(
        (
            "My assistant was supportive and helpful "
            "of both myself and the students."
        ),
        low_desc="agree",
        high_desc="disagree",
    )

    assistant_comments = models.TextField(
        "Comments about assistant:",
        blank=True,
    )

    suggestions = models.TextField(
        "Other comments/ideas for the future of Wonderment:",
        blank=True,
    )

    def __str__(self):
        return self.teacher_name
