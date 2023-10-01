from django.db import models
from accounts.models import Users


class Post(models.Model):
    CATEGORIES = [('Tech', 'Tech'),
                  ('News', 'News'),
                  ('ُSpecialized', 'Specialized'), ]
    title = models.CharField(max_length=250)
    description = models.TextField()
    category = models.CharField(choices=CATEGORIES, max_length=20, default='unknown')
    published = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=100)
    author = models.ForeignKey(Users, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title
