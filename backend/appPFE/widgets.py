from django.conf import settings
from django.forms.widgets import ClearableFileInput


class CustomClearableImageInput(ClearableFileInput):
    """
    A custom widget for ImageFields that customizes the standard behavior
    of ClearableFileInput.
    """
    template_name = 'appPFE/widgets/clearable_file_input.html'
    clear_checkbox_label = 'Delete image'  # Text for the checkbox
    input_text = 'Change'  # Text for the upload button

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Photo_portrait is stored as CharField (path string); build URL for preview
        if value:
            if hasattr(value, 'url'):
                context['widget']['image_url'] = value.url
            else:
                # value is a path string like "images/newaccount_11_picture.png"
                base = getattr(settings, 'MEDIA_URL', '/media/').rstrip('/')
                path = str(value).lstrip('/')
                context['widget']['image_url'] = f"{base}/{path}" if path else None
            # Parent only sets is_initial for File objects; with a string we must set it
            if context['widget'].get('image_url'):
                context['widget']['is_initial'] = True
        else:
            context['widget']['image_url'] = None
        return context
    
    def render(self, name, value, attrs=None, renderer=None):
        """
        Alternative: Completely custom render method.
        In case you do not want to use the template.
        """

        return super().render(name, value, attrs, renderer)
