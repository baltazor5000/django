from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from contacts.models import Contact
import forms

# Create your views here.
class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)

class ContactOwnerMixin(object):
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwargs, None)
        queryset = queryset.filter(
            pk=pk,
            owner = self.request.user,
        )
        try:
            obj = queryset.get()
        except ObjectDoesNonExist:
            raise PermissionDenied
        return obj

class ListContactView(LoggedInMixin, ContactOwnerMixin, ListView):
    model = Contact
    template_name = 'contact_list.html'
    
    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)

class CreateContactView(CreateView):
    fields = ['first_name', 'last_name', 'email', 'pic']
    model = Contact
    template_name = 'edit_contact.html'
    form_class = forms.ContactForm
    
    def get_success_url(self):
        return reverse('contacts-list')

    def get_context_data(self, **kwargs):
        context = super(CreateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-new')
        return context

class UpdateContactView(UpdateView):
    fields = ['first_name', 'last_name', 'email', 'pic']
    model = Contact
    template_name = 'edit_contact.html'
    form_class = forms.ContactForm
    
    def get_success_url(self):
        return reverse('contacts-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-edit',
                                    kwargs = {'pk': self.get_object().id})
        return context

class DeleteContactView(DeleteView):
    model = Contact
    template_name = 'delete_contact.html'
    
    def get_success_url(self):
        return reverse('contacts-list')

class ContactView(DetailView):
    model = Contact        
    template_name = 'contact.html'

class EditContactAddressView(UpdateView):
    model = Contact
    template_name = 'edit_addresses.html'
    form_class = forms.ContactAddressFormSet
    
    def get_success_url(self):
        return self.get_object().get_absolute_url()




