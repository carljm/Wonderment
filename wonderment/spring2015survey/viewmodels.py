from collections import Counter
from django.utils.functional import cached_property
from itertools import chain

from wonderment.fields import ArrayField
from . import models


class ResponseSummary(object):
    def __init__(self, responses):
        self.responses = responses

    @cached_property
    def questions(self):
        questions = []
        for field in self.fields:
            summary = self.summarize_field(field)
            if field.name.endswith('_other'):
                questions[-1]['other'] = summary['answers']
            else:
                questions.append(summary)
        return questions

    def summarize_field(self, field):
        data = {
            'name': field.name,
            'verbose_name': field.verbose_name,
        }
        answers = self.answers(field)
        if isinstance(field, models.RatingField):
            counts = Counter(answers)
            options = reversed([o[0] for o in field.choices])
            data.update({
                'type': 'rating',
                'counts': [(o, counts[o]) for o in options],
                'low_desc': field.low_desc,
                'high_desc': field.high_desc,
            })
        elif isinstance(field, ArrayField):
            data.update({
                'type': 'array',
                'counts': Counter(
                    self.expand(field, chain(*answers))).most_common(),
            })
        elif field.choices:
            data.update({
                'type': 'choices',
                'counts': Counter(
                    self.expand(field, answers)).most_common(),
            })
        else:
            data.update({'type': 'free', 'answers': answers})
        return data

    def expand(self, field, answers):
        choice_dict = dict(field.choices)
        return [choice_dict[a] for a in answers]

    def answers(self, field):
        answers = [
            getattr(r, field.attname) for r in self.responses
            if getattr(r, field.attname)
        ]
        return answers

    @cached_property
    def fields(self):
        omit = {'id', 'timestamp', 'parent'}
        return [f for f in models.Response._meta.fields if f.name not in omit]
