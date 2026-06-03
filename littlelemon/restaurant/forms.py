from django.forms import DateTimeInput, ModelForm

from .models import Booking


# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comment"].required = False
        self.input_type = "datetime-local"

    class Meta:
        model = Booking
        fields = "__all__"
        widgets = {"date_time": DateTimeInput(attrs={"type": "datetime-local"})}
