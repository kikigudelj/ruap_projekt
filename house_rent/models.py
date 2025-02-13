from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=50, null=True)
    surname = models.CharField(max_length=50, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username 

class House(models.Model):
    name = models.CharField(max_length=255, default="Kuća za najam")  
    address = models.CharField(max_length=255)
    year_built = models.PositiveIntegerField(default=2000)  
    num_rooms = models.PositiveIntegerField() 
    square_meters = models.PositiveIntegerField()  
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)  
    available = models.BooleanField(default=True)  
    description = models.TextField()  
    image = models.ImageField(upload_to='house_images/', blank=True, null=True)

    has_parking = models.BooleanField(default=False)  
    has_garden = models.BooleanField(default=False) 
    has_air_conditioning = models.BooleanField(default=False)  
    is_furnished = models.BooleanField(default=False)  

    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100) 

    created_at = models.DateTimeField(auto_now_add=True) 

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='houses')  # Veza s Django User modelom
    
    def __str__(self):
        return f"Kuća na {self.address}, {self.num_rooms} soba"


    
