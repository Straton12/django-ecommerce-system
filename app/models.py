from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.

STATE_CHOICES=(
    ('kerala','kerala'),('tamilnadu','tamilnadu'),('andrapredesh','andrapredesh'),('assam','assam'),
    ('bihar','bihar'),('delhi','delhi'),('gujarath','gujarath'),('utherpradesh','utharpradesh'),
    ('lakshadeep','lakshadeep'),('meezoram','meezoram'),('nagaland','nagaland'),
)

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)
    
    def __str__(self):
        return str(self.id)
    
CATEGORY_CHOICES=(
    ('M','mobile'),('L','laptop'),('TW','topwear'),('BW','bottomwear'),
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to='productimg')
    
    def __str__(self):
        return str(self.id)
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quatity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quatity * self.product.discounted_price
  
STATUS_CHOICES=(
    ('Accepted','Accepted'),('Packed','Packed'),('On the Way','On the Way'),
    ('Delivered','Delevered'),('Cancel','Cancel'),
) 
class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quatity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES,max_length=50,default='Pending')
    
    @property
    def total_cost(self):
        return self.quatity * self.product.discounted_price