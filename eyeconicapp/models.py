from django.db import models

# Create your models here.

class Product(models.Model):
    product_name=models.CharField(max_length=100)
    product_description=models.TextField()
    product_price=models.DecimalField(max_digits=10,decimal_places=2)
    product_image=models.ImageField(null=True,blank=True,upload_to='products/')



class UserRegistration(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    username=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    address=models.TextField()
    gender=models.CharField(max_length=10)
    pincode=models.CharField(max_length=10)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=15)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Cart(models.Model):
    user=models.ForeignKey(UserRegistration,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)

    def total_price(self):
        return self.product.product_price * self.quantity


class Order(models.Model):
    user=models.ForeignKey(UserRegistration,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    address=models.TextField()
    phone=models.CharField(max_length=15)
    ordered_at=models.DateTimeField(auto_now_add=True)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20,default='pending')
    

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    
class Wishlist(models.Model):
    user=models.ForeignKey(UserRegistration,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)







class Support(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  

    def __str__(self):
        return f"Support - {self.user.username} ({self.subject})"
