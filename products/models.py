from django.db import models
from django.utils.text import slugify

from categories.models import ProductCategory

class Product(models.Model):
    
    STATUS_CHOICES = (
        ('active','Active'),
        ('inactive','Inactive')
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    short_description = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='products/',blank=True,null=True)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    
    category  = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products')
    featured = models.BooleanField(default=False)
    
    sku = models.CharField(max_length=100, unique=True, null=True)    
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return self.name
    
    def generate_unique_slug(self):
        
        base_slug = slugify(self.name) or 'product'
        slug = base_slug
        counter = 1
        
        products = Product.objects.all()
        
        if self.id:
            products = products.exclude(id=self.id)
        
        while products.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        
        return slug
    
    def save(self, *args, **kwargs):
        self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)
    
