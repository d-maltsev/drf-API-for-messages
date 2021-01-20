from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import MessageViewSet, GeneratorCSV

router = SimpleRouter()
router.register(r'message', MessageViewSet, basename='message')

urlpatterns = [
    path('generate_csv/', GeneratorCSV.as_view(), name='generator'),
]
urlpatterns += router.urls
