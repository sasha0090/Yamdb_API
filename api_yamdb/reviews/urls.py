from django.urls import include, path

from rest_framework.routers import SimpleRouter

from . import views

app_name = 'reviews'

router_v1 = SimpleRouter()

router_v1.register(
    r'v1/titles/(?P<id>', views.CategoryViewSet, basename='title')
router_v1.register(
    r'v1/categories/(?P<id>', views.GenreViewSet, basename='category')
router_v1.register(
    r'v1/genres/(?P<id>', views.TitleViewSet, basename='genre')

urlpatterns = [
    path('', include(router_v1.urls)),
]
