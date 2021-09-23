from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

u1 = User.objects.first()
Product.objects.create(user=u1, title='My u1 product', price=12.99)

products_to_import = [
    {'title': 'product 1', 'price': 12.99},
    {'title': 'product 2', 'price': 14.99},
    {'title': 'product 3', 'price': 19.99},
]

first_product = products_to_import[0]

# create way 1
not_saved_obj = Product(title='another one', price=123.12)
not_saved_obj.save()

# create way 2
Product.objects.create(title='another one', price=123.12)

# unpackaged
Product(**first_product)

# bulk create
my_new_objs = []
for new_data in products_to_import:
    print(new_data)
    # Product(**new_data)
    my_new_objs.append(Product(**new_data))
Product.objects.bulk_create(my_new_objs, ignore_conflicts=True)


''' 
bulk delete
'''
qs = Product.objects.all()
qs.delete()


'''
delete single
'''
obj = Product.objects.first()
obj.delete()

# fixtures -> testing -> migrating data from databases

# psql, mysql

# python manage.py inspectdb -> convert database table to django model
