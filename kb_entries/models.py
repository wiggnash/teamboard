from django.db import models

class KBEntry(models.Model):
    class Category(models.TextChoices):
        API       = 'api',       'API'
        DATABASE  = 'database',  'Database'
        CLOUD     = 'cloud',     'Cloud'
        FRAMEWORK = 'framework', 'Framework'
        GENERAL   = 'general',   'General'

    question   = models.TextField()
    answer     = models.TextField()
    category   = models.CharField(max_length=20, choices=Category.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.question[:80]
