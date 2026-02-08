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
        """
        Overrides the context to add additional variables.
        """
        context = super().get_context(name, value, attrs)

        return context
    
    def render(self, name, value, attrs=None, renderer=None):
        """
        Alternative: Completely custom render method.
        In case you do not want to use the template.
        """

        return super().render(name, value, attrs, renderer)