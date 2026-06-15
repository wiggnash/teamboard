from django.urls import path

from .views import UsageSummaryView

# Routes for the query_logs app (usage summary).
urlpatterns = [
    path("admin/usage-summary/", UsageSummaryView.as_view(), name="usage-summary"),
]
