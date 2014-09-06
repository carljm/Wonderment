import csv

from . import models


FIELDS = {
    'first': 'First Name',
    'last': 'Last Name',
    'address': 'Address',
    'phone': 'Primary phone',
    'phone_type': 'Phone type',
    'email': 'Email',
    'preferred': 'Preferred method of communication',
    'level': 'I want to sign my child(ren) up for:',
    'participate_by': 'I am interested in participating by:',
    'age_groups': (
        'I feel most comfortable working with the following age groups:'),
    'could_teach': 'If you are interested in teaching...',
    'could_assist': 'If you are interested in assisting...',
    'all_ages_help': (
        'If you are interested in helping '
        'with the monthly all ages gathering...'
    ),
    'other_contributions': (
        'Other ideas/skills/contributions you might have to offer:'),
    'classes_desired': (
        'Any specific subjects/classes you hope other parents might be able '
        'to teach and that you would be most excited to sign your kids up for.'
    ),
    'num_kids': 'number of children to participate',
    'name1': 'full name of child 1 ',
    'age1': 'age of child 1',
    'gender1': 'gender of child 1',
    'name2': 'full name of child 2',
    'age2': 'age of child 2',
    'gender2': 'gender of child 2',
    'name3': 'full name of child 3',
    'age3': 'age of child 3',
    'gender3': 'gender of child 3',
    'name4': 'full name of child 4',
    'age4': 'age of child 4',
    'gender4': 'gender of child 4',
    'bday1': 'birthday for child 1',
    'bday2': 'birthday for child 2',
    'bday3': 'birthday for child 3',
    'bday4': 'birthday for child 4',
    'special1': 'allergies and special needs (ie potty training) for child 1',
    'special2': 'allergies and special needs (ie potty training) for child 2',
    'special3': 'allergies and special needs (ie potty training) for child 3',
    'special4': 'allergies and special needs (ie potty training) for child 4',
    'spouse': 'Spouse/Co-Guardian Name',
    'spouse_contact': 'Spouse/Co-Guardian contact',
    'emergency': 'Emergency Contact Name',
    'emergency_contact': 'Emergency Contact Number',
    'paid': 'Paid',
}

REV_FIELDS = {v: k for k, v in FIELDS.items()}


def import_csv(fn):
    with open(fn) as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            row = {REV_FIELDS[k]: v for k, v in row.items()}
            models.Parent.objects.create(
                name='%s %s' % (row['first'], row['last']),
            )
