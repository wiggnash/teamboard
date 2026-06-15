from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

        # 3. SEARCH — match the term in question OR answer (case-insensitive)
        results = KBEntry.objects.filter(
            Q(question__icontains=search_term) | Q(answer__icontains=search_term)
        )
        count = results.count()

        # TODO: 4. LOGGING

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
