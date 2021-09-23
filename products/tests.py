from django.test import TestCase
from django.utils.text import slugify
from .models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        ''' set up function '''
        self.create_draft_items()
        self.create_published_items()
        self.create_unique_slug_items()

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
        self.assertEqual(qs.count(), self.draft_count +
                         self.unique_slugs_count)

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

        #self.assertEqual(manager_qs.count(), self.pub_count)
        #self.assertEqual(custom_filter_qs.count(), self.pub_count)
        self.assertEqual(
            custom_filter_qs.count(),
            manager_qs.count(),
            self.pub_count,
        )

        # we use set for potential duplicated values
        manager_qs_ids = set(
            manager_qs.values_list('id', flat=True)
        )
        custom_filter_qs_ids = set(
            custom_filter_qs.values_list('id', flat=True)
        )  # utilizing the values_list func of qs
        self.assertEqual(manager_qs_ids, custom_filter_qs_ids)
        self.assertEqual(len(custom_filter_qs), 3)

    def create_unique_slug_items(self):
        ''' create mock items to slugify '''
        my_non_unique_title = 'Nulla et convallis lectus non congue lacus ac felis'
        data = {
            'title': my_non_unique_title,
            'price': 12.99,
        }
        self.slug_title = my_non_unique_title
        self.slugified_title = slugify(my_non_unique_title)
        self.slug_a = Product.objects.create(**data)
        self.slug_b = Product.objects.create(**data)
        self.slug_c = Product.objects.create(**data)
        self.unique_slugs_count = 3

    def test_slug_title_signal(self):
        ''' check generated slug is correct and the signal worked '''
        self.assertEqual(self.slug_a.slug, self.slugified_title)

    def test_slugs_unique(self):
        ''' check if generated slugs were unique '''
        self.assertNotEqual(
            self.slug_a.slug,
            self.slug_b.slug,
            self.slug_c.slug,
        )

    def test_slugs_unique_on_extra(self):
        ''' test if extra slugs were unique '''
        self.assertNotEqual(self.slugified_title, self.slug_b.slug)
        self.assertNotEqual(self.slugified_title, self.slug_c.slug)
        self.assertNotEqual(self.slug_b.slug, self.slug_c.slug)

    def test_original_slug_count(self):
        ''' check if original slug count is not equal to all unique slugs count '''
        qs = Product.objects.filter(slug=self.slugified_title)
        self.assertEqual(qs.count(), 1)  # original slug count
        self.assertNotEqual(qs.count(), self.unique_slugs_count)
