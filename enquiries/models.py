from django.db import models
from products.models import Product, ProductPriceVariation

class ProductEnquiry(models.Model):
    
    STATUS_CHOICES = (
        ('new','New'),
        ('contacted','Contacted'),
        ('closed','Closed')
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='enquiries'
    )
    
    variation = models.ForeignKey(
        ProductPriceVariation,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    
    name = models.CharField(max_length=100)
    
    email = models.EmailField(max_length=255)
    
    phone = models.CharField(max_length=15)
    
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    
    message = models.TextField(
        blank=True,
        null=True
    )
    
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='new')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.name} - {self.product.name}'
    