
from django import template

# create a teampate library object
register = template.Library()

# register the filter
@register.filter
def get_item(dictionary, key):
    """
    Gets a value from a dictionary.
    
    Example:
    translatable_fields = {'field_FR': 'field_EN'}
    {{ translatable_fields|get_item:'field_FR' }}  → returns 'field_EN' 
    """
    return dictionary.get(key)

# this function is used in the template, because we cannot write two underscores in html
@register.filter
def is_image_field(field):
    return field.field.__class__.__name__ == 'ImageField'