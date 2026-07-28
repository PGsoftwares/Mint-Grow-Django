from django.db import models
from django.utils.text import slugify

class ProductCategory(models.Model):
    
    STATUS_CHOICES = (
        ('active','Active'),
        ('inactive','Inactive')
    )
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        blank=True,
        null=True
    )
    
    slug = models.SlugField(max_length=255, blank=True, null=True)
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    
    
    class Meta:
        ordering = ['parent_id','name']
        
        constraints = [
            models.UniqueConstraint(
                fields=['parent','name'],
                name = 'unique_category_name_under_parent'                
            )
        ]
        
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categoreis'
        
        
    def __str__(self):
        return self.full_name
    
    
    @property
    def full_name(self):
        names = [self.name]
        parent = self.parent
        
        while parent:
            names.insert(0, parent.name)
            parent = parent.parent
        
        return '->'.join(names)
    
    
    @property
    def level(self):
        level = 0
        parent = self.parent
        
        while parent:
            level += 1
            parent = parent.parent
        
        return level
    
    def save(self, *args, **kwargs):
        self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)


    def generate_unique_slug(self):
        base_slug = slugify(self.name) or "category"
        slug = base_slug
        counter = 1

        queryset = ProductCategory.objects.exclude(pk=self.pk)

        while queryset.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug