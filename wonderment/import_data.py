import csv

from dateutil import parser

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


def import_csv(session, fn):
    with open(fn) as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            row = {REV_FIELDS[k]: v for k, v in row.items() if k in REV_FIELDS}
            parent = models.Parent(
                name='%s %s' % (row['first'], row['last']),
                address=row['address'],
                phone=row['phone'],
                phone_type=clean_phone_type(row['phone_type']),
                email=row['email'],
                preferred=clean_choice_field(row['preferred'], 'preferred'),
                age_groups=row['age_groups'],
                could_teach=row['could_teach'],
                could_assist=row['could_assist'],
                all_ages_help=row['all_ages_help'],
                other_contributions=row['other_contributions'],
                classes_desired=row['classes_desired'],
                spouse=row['spouse'],
                spouse_contact=row['spouse_contact'],
                emergency=row['emergency'],
                emergency_contact=row['emergency_contact'],
            )
            parent.full_clean(validate_unique=False)
            parent.save(force_insert=True)

            participant = models.Participant(
                parent=parent,
                session=session,
                paid=clean_int(row['paid']),
                level=clean_level(row['level']),
            )
            participant.full_clean(validate_unique=False)
            participant.save(force_insert=True)

            for num in [1, 2, 3, 4]:
                if row['name%s' % num]:
                    child = models.Child(
                        parent=parent,
                        name=row['name%s' % num],
                        gender=clean_gender(row['gender%s' % num]),
                        birthdate=clean_date(row['bday%s' % num]),
                        special_needs=row['special%s' % num],
                    )
                    child.full_clean(validate_unique=False)
                    child.save(force_insert=True)


def clean_phone_type(v):
    v = v.lower()
    if v in {'cellular', 'mobile'}:
        v = 'cell'
    return clean_choice_field(v, 'phone_type')


def clean_level(v):
    if v == "ALL fall classes":
        v = 'weekly'
    elif v == "Monthly all ages gatherings ONLY":
        v = 'monthly'
    return clean_choice_field(v, 'level', models.Participant)


def clean_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def clean_gender(v):
    v = v.lower()
    if v in {'m', 'boy'}:
        v = 'male'
    elif v in {'f', 'girl'}:
        v = 'female'
    return clean_choice_field(v, 'gender', model=models.Child)


def clean_date(v):
    return parser.parse(v) if v else None


def clean_choice_field(v, field_name, model=models.Parent):
    v = v.lower()
    field = model._meta.get_field_by_name(field_name)[0]
    if v not in {c[0] for c in field.choices}:
        v = ''
    return v
