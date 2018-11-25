from django import template

register = template.Library()


@register.inclusion_tag('favorite_button.html')
def show_buttons(book, user):

    if book in [favorite.book for favorite in user.favorite_set.all()]:
        return {
            'slug': book.slug,
            'liked': True
        }
    else:
        return {
            'slug': book.slug,
            'liked': False
            }
