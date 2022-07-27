import csv
import os

import django
from django.contrib.auth import get_user_model

from reviews.models import Category, Comment, Genre, Review, Title

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_yamdb.settings")


django.setup()


User = get_user_model()


data = {
    "users.csv": {
        User: "User(id=row['id'],"
        "username=row['username'],"
        "email=row['email'],"
        "role=row['role'])"
    },
    "category.csv": {
        Category: "Category(id=row['id'],name=row['name'],slug=row['slug'])"
    },
    "genre.csv": {
        Genre: "Genre(id=row['id'],name=row['name'],slug=row['slug'])"
    },
    "titles.csv": {
        Title: "Title(id=row['id'],"
        "name=row['name'],"
        "year=row['year'],"
        "category=Category.objects.get(pk=row['category']))"
    },
    "genre_title.csv": {
        Title.genre.through: "Title.genre.through("
        "title_id=row['title_id'], "
        "genre_id=row['genre_id'])"
    },
    "review.csv": {
        Review: "Review(id=row['id'],"
        "title=Title.objects.get(pk=row['title_id']),"
        "text=row['text'],author=User.objects.get(pk=row['author']),"
        "score=row['score'],pub_date=row['pub_date'])"
    },
    "comments.csv": {
        Comment: "Comment(id=row['id'],"
        "review=Review.objects.get(pk=row['review_id']),"
        "text=row['text'],author=User.objects.get(pk=row['author']),"
        "pub_date=row['pub_date'])"
    },
}


def create_users(csv_name, create_code):
    """Создание dummy data для пользователей из csv файла"""
    with open(f"./static/data/{csv_name}", "r", encoding="utf-8") as csvfile:
        dr = csv.DictReader(csvfile)
        return [eval(create_code) for row in dr]


for csv_name, create_data in data.items():
    model = list(create_data.keys())[0]
    create_code = list(create_data.values())[0]
    print(f"Записываем {csv_name}...")
    model.objects.bulk_create(create_users(csv_name, create_code))
