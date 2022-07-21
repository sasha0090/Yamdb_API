from django.urls import include, path

from rest_framework.routers import SimpleRouter

from . import views

app_name = 'reviews'

router_v1 = SimpleRouter()

router_v1.register(
    r'v1/titles', views.TitleViewSet, basename='title')
router_v1.register(
    r'v1/categories', views.CategoryViewSet, basename='category')
router_v1.register(
    r'v1/genres', views.GenreViewSet, basename='genre')

urlpatterns = [
    path('', include(router_v1.urls)),
]
