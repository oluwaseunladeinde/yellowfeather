from django.utils.translation import ugettext_lazy as _

TYPES = (
    ('house', _('Houses')),
    ('villa', _('Villas')),
    ('penthouse', _('Penthouses')),
    ('apartment', _('Apartments')),
    ('residencial-land', _('Residential Land')),
    ('corporate-office', _('Corporate Offices')),
    ('commercial-office', _('Commercial Offices')),
    ('commercial-space', _('Commercial Space')),
    ('industrial-building', _('Industrial Buildings')),
    ('commercial-warehouses', _('Commercial Warehouses')),
    ('commercial-land', _('Commercial Land')),
)

BATHROOMS_RANGE = (
    ('', '--'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6+'),
)

BEDROOMS_RANGE = (
    ('', '--'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6+'),
)

LOCATION_STREET = 'street'
LOCATION_SECTOR = 'sector'
LOCATION_CITY = 'city'
LOCATION_STATE = 'state'

LOCATION_TYPES = (
    (LOCATION_STREET, _('Street')),
    (LOCATION_SECTOR, _('Sector')),
    (LOCATION_CITY, _('City')),
    (LOCATION_STATE, _('State/Province')),
)

OFFERS = (
    ('', '--'),
    ('buy', _('For Sale')),
    ('rent', _('For Rent')),
    ('buy-rent', _('For Sale/For Rent'))
)

NIGERIA_STATES = (
    ('abia', 'Abia'), ('abuja', 'Abuja FCT'), ('adamawa', 'Adamawa'), ('akwaibom', 'Akwa Ibom'), ('anambra', 'Anambra'),
    ('bauchi', 'Bauchi'), ('bayelsa', 'Bayelsa'), ('benue', 'Benue'), ('borno', 'Borno'), ('crossriver', 'Cross River'),
    ('delta', 'Delta'), ('ebonyi', 'Ebonyi'), ('edo', 'Edo'), ('ekiti', 'Ekiti'), ('enugu', 'Enugu'),
    ('gombe', 'Gombe'), ('imo', 'Imo'), ('jigawa', 'Jigawa'), ('kaduna', 'Kaduna'), ('kano', 'Kano'),
    ('katsina', 'Katsina'), ('kebbi', 'Kebbi'), ('kogi', 'Kogi'), ('kwara', 'Kwara'), ('lagos', 'Lagos'),
    ('nassarawa', 'Nassarawa'), ('niger', 'Niger'), ('ogun', 'Ogun'), ('osun', 'Osun'), ('oyo', 'Oyo'),
    ('plateau', 'Plateau'), ('rivers', 'Rivers'), ('sokoto', 'Sokoto'), ('taraba', 'Taraba'),
    ('yobe', 'Yobe'), ('zamfara', 'Zamfara'),
)
