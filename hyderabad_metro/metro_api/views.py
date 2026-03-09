from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

from .metro_graph import find_shortest_path, get_all_stations
from .serializers import PathRequestSerializer, PathResponseSerializer, StationSerializer


def index(request):
    """Serve the main HTML frontend."""
    stations = get_all_stations()
    return render(request, 'metro_api/index.html', {'stations': stations})


class StationListView(APIView):
    """
    GET /api/stations/
    Returns list of all Hyderabad metro stations.
    """

    def get(self, request):
        stations = get_all_stations()
        serializer = StationSerializer(stations, many=True)
        return Response({
            "count": len(stations),
            "stations": serializer.data
        })


class ShortestPathView(APIView):
    """
    POST /api/shortest-path/
    Find shortest path between two metro stations.

    Request body:
    {
        "source": "ameerpet",
        "destination": "hitec_city",
        "optimize": "time"  // or "distance"
    }
    """

    def post(self, request):
        serializer = PathRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"error": "Invalid input", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        source = serializer.validated_data['source']
        destination = serializer.validated_data['destination']
        optimize = serializer.validated_data['optimize']

        result = find_shortest_path(source, destination, optimize)

        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)

    def get(self, request):
        """Support GET with query params for browser testing."""
        source = request.query_params.get('source')
        destination = request.query_params.get('destination')
        optimize = request.query_params.get('optimize', 'time')

        if not source or not destination:
            return Response(
                {"error": "Please provide 'source' and 'destination' query parameters"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = find_shortest_path(source, destination, optimize)
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)
