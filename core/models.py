from django.db import models



class Customer(models.Model):
    EMIRATES = [
        ('abudhabi', 'Abu Dhabi'),
        ('dubai', 'Dubai'),
        ('sharjah', 'Sharjah'),
        ('ajman', 'Ajman'),
        ('ummalquwain', 'Umm Al Quwain'),
        ('rasalkhaimah', 'Ras Al Khaimah'),
        ('fujairah', 'Fujairah')
        
    ]
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    dob = models.DateField()
    emirate = models.CharField(choices=EMIRATES, default='dubai')
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True) 
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name
