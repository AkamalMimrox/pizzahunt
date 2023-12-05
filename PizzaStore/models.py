from django.db import models
from PizzaStore.custom.slug_genrate import generate_random_slug
from UserAuth.models import UserAuthMaster
from django_countries.fields import CountryField


# Create your models here.


class CategoriesMaster(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)

    def save(self, *args, **krgs):
        if not self.slug:
            while True:
                slug = generate_random_slug(self.name)
                if not CategoriesMaster.objects.filter(slug=slug).exists():
                    self.slug = slug
                    break
        super().save(*args, **krgs)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return


class ProductMaster(models.Model):
    category = models.ForeignKey(CategoriesMaster,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="Product")
    price = models.IntegerField()
    slug = models.SlugField(editable=False)

    def save(self, *args, **krgs):
        if not self.slug:
            while True:
                slug = generate_random_slug(self.name)
                if not ProductMaster.objects.filter(slug=slug).exists():
                    self.slug = slug
                    break
        super().save(*args, **krgs)
                
    def __str__(self):
        return self.name


class about(models.Model):
    location = models.CharField(max_length=1000)
    contactnumber = models.CharField(max_length=20)
    email = models.EmailField()
    socialmedia=models.ManyToManyField('Social',related_name='about')
    openinghours=models.CharField(max_length=50)
    copyright=models.CharField(max_length=50)
    distributedby=models.CharField(max_length=20)
    
    
    def __str__(self):
        return self.email
    

class Social(models.Model):
    name=models.CharField(default='facebook',choices=[('facebook','Facebook'),('twitter','Twitter'),('linkedin','Linkedin'),('instagram','Instagram'),('pinterest',"Pinterest")])
    link=models.URLField()
    
    def __str__(self):
        return self.link
    


class AddressMaster(models.Model):
    user = models.ForeignKey(UserAuthMaster,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phonenumber = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()
    country = CountryField()
    
    def __str__(self):
        return self.first_name
    
    
class PaymentStatus(models.Model):
    status = models.CharField(choices=[("pending","Pending"),("confirm","Confirm"),("cancle","Cancle")],default='pending')
    def __str__(self):
        return self.status
    
class Order(models.Model):
    id = models.CharField(primary_key=True,max_length=100)
    user = models.ForeignKey(UserAuthMaster,on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=100)
    shiping_address = models.ForeignKey(AddressMaster,on_delete=models.CASCADE)
    order_total = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.tracking_number
    

class OrderItem(models.Model):
    user = models.ForeignKey(UserAuthMaster,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductMaster,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)
    price = models.CharField(default=None,max_length=10000)
    
    def __str__(self):
        return self.user