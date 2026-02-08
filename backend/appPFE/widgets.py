from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe
from django.utils.html import format_html


class CustomClearableImageInput(ClearableFileInput):
    """
    A custom widget for ImageFields that customizes the standard behavior
    of ClearableFileInput.
    """
    template_name = 'appPFE/widgets/clearable_file_input.html'
    clear_checkbox_label = 'Delete image'  # Text for the checkbox
    input_text = 'Change'  # Text for the upload button
    
    def get_context(self, name, value, attrs):
        """
        Overrides the context to add additional variables.
        """
        context = super().get_context(name, value, attrs)
        # Here you can add additional variables to the context
        return context
    
    def render(self, name, value, attrs=None, renderer=None):
        """
        Alternative: Completely custom render method.
        In case you do not want to use the template.
        """
        # If you want to use the default template, call super():
        return super().render(name, value, attrs, renderer)
        
        # OR: Completely custom HTML generation:
        # html = []
        # if value and hasattr(value, 'url'):
        #     html.append(f'<p>Currently: <a href="{value.url}">{value.name}</a></p>')
        #     html.append(f'<input type="checkbox" name="{name}-clear" id="{name}-clear">')
        #     html.append(f'<label for="{name}-clear">Delete image</label>')
        # html.append(f'<input type="file" name="{name}">')
        # return mark_safe(''.join(html))
