from django.urls import reverse
from django.db import models
from category_app.models import Category


# Create your models here.

class Product(models.Model):
    product_name   = models.CharField(max_length=200, unique=True)
    slug           = models.SlugField(max_length=200, unique=True)
    description    = models.TextField(max_length=500, unique=True)
    price          = models.IntegerField()
    images         = models.ImageField(upload_to='photo/products')
    stock          = models.IntegerField()
    is_available   = models.BooleanField(default=True)
    category       = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date   = models.DateTimeField(auto_now_add=True)
    modified_date  = models.DateTimeField(auto_now=True)

    # takeing url of perticular category and product
        # it is for global use also
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name