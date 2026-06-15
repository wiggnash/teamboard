from django.db import transaction
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from query_logs.models import QueryLog

from .models import KBEntry
from .serializers import KBQuerySerializer, KBEntrySerializer


class KBQueryView(APIView):
    def post(self, request):
        # 1. VALIDATE
        serializer = KBQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        search_term = serializer.validated_data["search"]

        # 2. IDENTITY
        company = request.user.company

        # 3 & 4. SEARCH + LOGGING
        with transaction.atomic():
            # match the term in question OR answer (case-insensitive)
            results = KBEntry.objects.filter(
                Q(question__icontains=search_term) | Q(answer__icontains=search_term)
            )
            count = results.count()

            # log the search
            QueryLog.objects.create(
                company=company,
                search_term=search_term,
                results_count=count,
            )

        # 5. RESPONSE
        results_data = KBEntrySerializer(results, many=True).data
        return Response(
            {
                "search": search_term,
                "count": count,
                "results": results_data,
            },
            status=status.HTTP_200_OK,
        )
