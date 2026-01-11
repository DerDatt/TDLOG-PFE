
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