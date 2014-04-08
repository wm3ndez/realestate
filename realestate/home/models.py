from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField()
    active = models.BooleanField(default=False)
    tags = models.CharField(max_length=255)
    featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Articule'
        verbose_name_plural = 'News'

    def __unicode__(self):
        return self.title


class Contacts(models.Model):
    name = models.CharField(max_length=60)
    phone = models.CharField(max_length=20)
    cellphone = models.CharField(max_length=20)
    email = models.EmailField()
    info = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'

    def __unicode__(self):
        return self.name


class Links(models.Model):
    name = models.CharField(max_length=32)
    link = models.URLField(max_length=255)
    description = models.CharField(max_length=150)
    contact = models.OneToOneField(Contacts)
    active = models.BooleanField(default=False)

    def get_url(self):
        if self.link.startswith('http'):
            return self.link
        return 'http://' + self.link

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    def __unicode__(self):
        return self.name
