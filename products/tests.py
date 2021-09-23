from django.test import TestCase
from .models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        ''' set up function '''
        self.create_draft_items()
        self.create_published_items()

    def create_draft_items(self):
        ''' create some mock DRAFT items '''
        data = {
            'title': 'Draft item',
            'price': 12.99
        }
        self.draft_a = Product.objects.create(**data)
        self.draft_b = Product.objects.create(**data)
        self.draft_c = Product.objects.create(**data)

        self.draft_count = 3

    def test_queryset_exists(self):
        ''' test if some products were found '''
        qs = Product.objects.all()
        self.assertTrue(qs.exists())

    def test_draft_count(self):
        ''' test created DRAFT items count '''
        qs = Product.objects.filter(state=Product.PublishStateOptions.DRAFT)
        #self.assertTrue(qs.count() == self.draft_count)
        self.assertEqual(qs.count(), self.draft_count)

    def create_published_items(self):
        ''' create mock published items '''
        data = {
            'title': 'Draft item',
            'price': 12.99,
            'state': Product.PublishStateOptions.PUBLISH
        }
        self.pub_a = Product.objects.create(**data)
        self.pub_b = Product.objects.create(**data)
        self.pub_c = Product.objects.create(**data)
        self.pub_count = 3

    def test_pub_count(self):
        ''' testing created published product count '''
        qs = Product.objects.filter(state=Product.PublishStateOptions.PUBLISH)
        self.assertEqual(qs.count(), self.pub_count)

    def test_pub_prop(self):
        ''' test if the `is_published` property is True for the published items '''
        self.assertTrue(self.pub_a.is_published)
        self.assertTrue(self.pub_b.is_published)
        self.assertTrue(self.pub_c.is_published)

    # def test_pub_count_manager(self):
    #    ''' test if the custom manager published method is working '''
    #    qs = Product.objects.published()
    #    self.assertEqual(qs.count(), self.pub_count)

    # def test_pub_count_qs_filter(self):
    #    ''' test if the custom QuerySet published filter working '''
    #    qs = Product.objects.all().published()
    #    self.assertEqual(qs.count(), self.pub_count)

    def test_publish_count_manager_qs_filter(self):
        '''
        test if the custom manager published method is working
        test if the custom QuerySet published filter working
        '''
        manager_qs = Product.objects.published()
        custom_filter_qs = Product.objects.all().published()

        self.assertEqual(manager_qs.count(), self.pub_count)
        self.assertEqual(custom_filter_qs.count(), self.pub_count)
        self.assertEqual(custom_filter_qs.count(), manager_qs.count())

        # we use set for potential duplicated values
        manager_qs_ids = set(
            manager_qs.values_list('id', flat=True)
        )
        custom_filter_qs_ids = set(
            custom_filter_qs.values_list('id', flat=True)
        )  # utilizing the values_list func of qs
        self.assertEqual(manager_qs_ids, custom_filter_qs_ids)
