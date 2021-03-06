from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(
        max_length=255,)
   
    last_name = models.CharField(
        max_length=255,)
   
    email = models.EmailField()
    owner = models.ForeignKey(User)
    
    pic = models.ImageField("Image", upload_to="images/", default='')
    upload_date = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('contacts-view', kwargs={'pk': self.id})


class AddressType(models.Model):
    type = models.CharField(
        max_length=30,)

    def __str__(self):
        return '%s' % self.type


class Address(models.Model):
    contact = models.ForeignKey(Contact)
    
    address_type = models.ForeignKey(AddressType)

    address = models.CharField(
        max_length=255,)

    city = models.CharField(
        max_length=255,)

    state = models.CharField(
        max_length=2,)

    postal_code = models.CharField(
        max_length=20,)

    class Meta:
        unique_together = ('contact', 'address_type')