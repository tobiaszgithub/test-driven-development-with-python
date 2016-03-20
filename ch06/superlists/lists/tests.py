from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertTrue(response.content.decode(), expected_html)
        
        #=======================================================================
        # self.assertIn('A new list item',response.content.decode())
        # expected_html = render_to_string('home.html', {
        #                 'new_item_text': request.POST.get('item_text', ''),
        #                 }, request=request)
        # self.assertEqual(response.content.decode(), expected_html)
        #=======================================================================

    

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'list.html')
    def test_all_list_items(self):
        Item.objects.create(text="item 1")
        Item.objects.create(text="item 2")
        
        response = self.client.get('/lists/the-only-list/')
        
        self.assertContains(response, "item 1" )
        self.assertContains(response, "item 2" )    
        
    def test_saving_a_POST_request(self):
        
        self.client.post('/lists/new', data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, 'A new list item')
        
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', 
                                    data={'item_text':'A new list item'})
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/the-only-list/')
        
class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()
        
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()
        
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        
        self.assertEqual(first_saved_item.text, 'The first (ever) list item' )
        self.assertEqual(second_saved_item.text, 'Item the second' )
        
        