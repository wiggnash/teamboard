from django.urls import path

from .views import KBQueryView

# Routes for the kb_entries app (kb query).
urlpatterns = [
    path("query/", KBQueryView.as_view(), name="kb-query"),
]
