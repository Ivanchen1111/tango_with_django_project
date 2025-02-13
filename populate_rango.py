import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
django.setup()

# Import the models
from rango.models import Category, Page

def populate():
    # Define the pages and categories
    python_pages = [
        {'title': 'Official Python Tutorial', 'url': 'http://docs.python.org/3/tutorial/'},
        {'title': 'How to Think like a Computer Scientist', 'url': 'http://www.greenteapress.com/thinkpython/'},
        {'title': 'Learn Python in 10 Minutes', 'url': 'http://www.korokithakis.net/tutorials/python/'}
    ]

    django_pages = [
        {'title': 'Official Django Tutorial', 'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
        {'title': 'Django Rocks', 'url': 'http://www.djangorocks.com/'},
        {'title': 'How to Tango with Django', 'url': 'http://www.tangowithdjango.com/'}
    ]

    other_pages = [
        {'title': 'Bottle', 'url': 'http://bottlepy.org/docs/dev/'},
        {'title': 'Flask', 'url': 'http://flask.pocoo.org'}
    ]

    categories = {
        'Python': {'pages': python_pages},
        'Django': {'pages': django_pages},
        'Other Frameworks': {'pages': other_pages}
    }

    # Create categories and add pages to each
    for category_name, category_data in categories.items():
        cat = add_category(category_name)
        for page in category_data['pages']:
            add_page(cat, page['title'], page['url'])

    # Print what was added
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(category, title, url, views=0):
    p, created = Page.objects.get_or_create(category=category, title=title)
    p.url = url
    p.views = views
    p.save()
    return p

def add_category(name):
    c, created = Category.objects.get_or_create(name=name)
    c.save()
    return c

# Start execution
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
