CONTACT_FORM_INDUSTRIES = [
    'Advanced engineering',
    'Aerospace',
    'Agriculture, horticulture, fisheries and pets',
    'Airports',
    'Automotive',
    'Chemicals',
    'Construction',
    'Consumer and retail',
    'Creative industries',
    'Defence',
    'Education and training',
    'Energy',
    'Environment',
    'Financial and professional services',
    'Food and drink',
    'Healthcare services',
    'Maritime',
    'Medical devices and equipment',
    'Mining',
    'Pharmaceuticals and biotechnology',
    'Railways',
    'Security',
    'Space',
    'Sports economy',
    'Technology and smart cities',
    'Water',
]

INDUSTRY_CHOICES = [('', 'Please select')] + [(item, item) for item in CONTACT_FORM_INDUSTRIES] + [('OTHER', 'Other')]

INDUSTRY_MAP = dict(INDUSTRY_CHOICES)
