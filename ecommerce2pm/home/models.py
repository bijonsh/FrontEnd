from django.conf import settings
from django.db import models
from django.urls import reverse

STOCK = (('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock'))
LABELS = (('new', 'New'),('sale','Sale'),{'hot','Hot'})
STATUS = (('active', 'Active'), ('', 'Default'))
# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to= 'images')
    slug = models.TextField()
    brand = models.CharField(max_length=100, blank = True)
    stock = models.CharField(max_length=100, choices=STOCK)
    labels = models.CharField(max_length=100, choices=LABELS)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("home:product", kwargs = {'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("home:add-to-cart", kwargs={'slug': self.slug})


class Slider(models.Model):
    title = models.CharField(max_length=100)
    image = models.TextField()
    rank = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS, blank=True)
    description =models.TextField()
    caption_one = models.CharField(max_length=200)
    caption_two = models.CharField(max_length=200)
    caption_three = models.CharField(max_length=200)
    caption_four = models.CharField(max_length = 100, default = "caption")

    def __str__(self):
        return self.title

class Ad(models.Model):
    title = models.CharField(max_length=100)
    image = models.TextField()
    rank = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS, blank=True)

    def __str__(self):
        return self.title

class Brand(models.Model):
    title = models.CharField(max_length=100)
    image = models.TextField()
    description = models.TextField()
    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
       return self.item.title

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models. ManyToManyField(OrderItem)

    def __str__(self):
       return self.user.username

