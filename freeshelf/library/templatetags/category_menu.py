from django import template
from library.models import Category

register = template.Library()


@register.inclusion_tag('category_menu.html')
def category_menu():
    categories = Category.objects.all()
    return {
        'categories': categories
    }
