from django.core.management.base import BaseCommand
from django.conf import settings
import os.path
import json
from library.models import Book
from django.core.files import File
from django.template.defaultfilters import slugify


def get_path(file):
    return os.path.join(settings.BASE_DIR, 'book_data', file)


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Book.objects.all().delete()

        with open(get_path('books.json'), 'r') as file:
            reader = json.load(file)

            i = 0

            for book in reader:

                book = Book(
                    title=reader[i]['title'],
                    author=reader[i]['author'],
                    description=reader[i]['description'],
                    url=reader[i]['url'],
                    slug=slugify(reader[i]['title'])
                )
                if 'image' in reader[i]:
                    book.image.save(reader[i]['image'],
                                    File(open(get_path(
                                        reader[i]['image']), 'rb')))
                book.save()
                print(f"Imported {reader[i]['title']}")
                i += 1
