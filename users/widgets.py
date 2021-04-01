from django.forms import DateTimeInput

# calendar widget for selecting date of birth in sign up field
class XDSoftDateTimePickerInput(DateTimeInput):
    template_name = 'widgets/xdsoft_datetimepicker.html'
