from django.test import TestCase, LiveServerTestCase
from django.test.client import Client
from django.test.client import RequestFactory
from contacts.models import Contact
from contacts.views import ListContactView
from selenium.webdriver.firefox.webdriver import WebDriver
from rebar.testing import flatten_to_dict
from contacts import forms

# Create your tests here.
class ContactTestCase(TestCase):
    """Contact model tests."""
    def test_str(self):
        contact = Contact(first_name="John", last_name="Doe")
        self.assertEquals(
            str(contact),
            'John Doe',
        )

class ContactListViewTests(TestCase):
    """Contact list view tests"""
    
    def test_contacts_in_the_context(self):
        client = Client()
        response = client.get('/')
        self.assertEquals(list(response.context['object_list']), [])
        Contact.objects.create(first_name='foo', last_name='bar')
        response = client.get('/')
        self.assertEquals(response.context['object_list'].count(), 1)

    def test_contacts_in_the_context_request_factory(self):
        factory = RequestFactory()
        requst = factory.get('/')
        response = ListContactView.as_view()(requst)
        self.assertEquals(list(response.context_data['object_list']), [])
        Contact.objects.create(first_name='foo', last_name='bar')
        response = ListContactView.as_view()(requst)
        self.assertEquals(response.context_data['object_list'].count(), 1)

class ContactListIntegrationTests(LiveServerTestCase):
    """Contact list integration test"""
    
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(ContactListIntegrationTests, cls).setUpClass()


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ContactListIntegrationTests, cls).tearDownClass()

    def test_contact_listed(self):
        Contact.objects.create(first_name='foo', last_name='bar')
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertEquals(
            self.selenium.find_elements_by_css_selector('.contact')[0].text,
            'foo bar (edit) (delete)'
        )

    def test_add_contact_linked(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assert_(
            self.selenium.find_elements_by_link_text('add contact')
        )

    def test_add_contact(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_link_text('add contact').click()
        self.selenium.find_element_by_id('id_first_name').send_keys('test')
        self.selenium.find_element_by_id('id_last_name').send_keys('contact')
        self.selenium.find_element_by_id('id_email').send_keys('test@example.com')
        self.selenium.find_element_by_id('id_confirm_email').send_keys('test@example.com')
        self.selenium.find_element_by_id('save_contact').click()
        self.assertEquals(
            self.selenium.find_elements_by_css_selector('.contact')[-1].text,
            'test contact (edit) (delete)'
        )

class EditContactFormTest(TestCase):
    """Contact list test form"""
    
    def test_mismatch_email_is_invalid(self):
        form_data = flatten_to_dict(forms.ContactForm())
        form_data['first_name'] = 'foo'
        form_data['last_name'] = 'bar'
        form_data['email'] = 'foo@example.com'
        form_data['confirm_email'] = 'bar@example.com'
        
        bound_form = forms.ContactForm(data=form_data)
        self.assertFalse(bound_form.is_valid())
        
    def test_same_email_is_valid(self):
        form_data = flatten_to_dict(forms.ContactForm())
        form_data['first_name'] = 'foo'
        form_data['last_name'] = 'bar'
        form_data['email'] = 'foo@example.com'
        form_data['confirm_email'] = 'foo@example.com'
        
        bound_form = forms.ContactForm(data=form_data)
        self.assert_(bound_form.is_valid())
        


