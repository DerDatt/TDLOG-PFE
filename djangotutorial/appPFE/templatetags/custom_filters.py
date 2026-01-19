
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

@register.filter
def get_key_for_value(dictionary, value):
    """
    Finds the key in a dictionary that has the given value.
    
    Example:
    translatable_fields = {'__Presentation_contexte_FR__': '__Presentation_contexte_EN__'}
    {{ translatable_fields|get_key_for_value:'__Presentation_contexte_EN__' }}  → returns '__Presentation_contexte_FR__'
    """
    for key, val in dictionary.items():
        if val == value:
            return key
    return None