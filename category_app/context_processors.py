# for category showing 
# addit to setting .py

from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)