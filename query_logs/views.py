from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from companies.permissions import IsAdminUser

from .models import QueryLog


class UsageSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # total queries ever made — collapse the whole table to one number
        total_queries = QueryLog.objects.aggregate(total=Count("id"))["total"]

        # how many distinct companies have ever queried
        active_companies = QueryLog.objects.values("company").distinct().count()

        # top 5 most-searched terms — group by search_term, count each group
        top_search_terms = (
            QueryLog.objects.values("search_term")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        )

        return Response(
            {
                "total_queries": total_queries,
                "active_companies": active_companies,
                "top_search_terms": top_search_terms,
            },
            status=status.HTTP_200_OK,
        )
