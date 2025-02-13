from django import forms
from .models import House

class HouseRentalForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['name', 'address','year_built', 'num_rooms', 'square_meters', 'price_per_month', 'description', 'image', 'has_parking', 'has_garden', 'has_air_conditioning', 'is_furnished', 'city', 'neighborhood']

class HouseRentForm(forms.Form):
    area = forms.IntegerField(label='Area', required=True)
    room_num = forms.IntegerField(label='Number of Rooms', required=True)
    floor = forms.IntegerField(label='Floor', required=True)
    total_floor = forms.IntegerField(label='Total Floors', required=True)
    year_built = forms.IntegerField(label='Year Built', required=True)

    CHOICES = [(0, 'No'), (1, 'Yes')]

    balcony = forms.TypedChoiceField(label='Balcony', choices=CHOICES, coerce=int, required=True)
    basement = forms.TypedChoiceField(label='Basement', choices=CHOICES, coerce=int, required=True)
    dish_washer = forms.TypedChoiceField(label='Dish Washer', choices=CHOICES, coerce=int, required=True)
    fridge = forms.TypedChoiceField(label='Fridge', choices=CHOICES, coerce=int, required=True)
    furniture = forms.TypedChoiceField(label='Furniture', choices=CHOICES, coerce=int, required=True)
    tv_set = forms.TypedChoiceField(label='TV Set', choices=CHOICES, coerce=int, required=True)
    air_conditioning = forms.TypedChoiceField(label='Air Conditioning', choices=CHOICES, coerce=int, required=True)
    elevator = forms.TypedChoiceField(label='Elevator', choices=CHOICES, coerce=int, required=True)
    garage_parking = forms.TypedChoiceField(label='Garage Parking', choices=CHOICES, coerce=int, required=True)
    secure_doors_windows = forms.TypedChoiceField(label='Secure Doors/Windows', choices=CHOICES, coerce=int, required=True)
    monitoring_security = forms.TypedChoiceField(label='Monitoring/Security', choices=CHOICES, coerce=int, required=True)
    internet = forms.TypedChoiceField(label='Internet', choices=CHOICES, coerce=int, required=True)