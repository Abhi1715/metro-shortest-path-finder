from rest_framework import serializers


class PathRequestSerializer(serializers.Serializer):
    source = serializers.CharField(max_length=100, help_text="Source station ID")
    destination = serializers.CharField(max_length=100, help_text="Destination station ID")
    optimize = serializers.ChoiceField(
        choices=[('time', 'Fastest Route'), ('distance', 'Shortest Distance')],
        default='time',
        help_text="Optimization criteria"
    )


class StationSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    line = serializers.ListField(child=serializers.CharField())


class PathStepSerializer(serializers.Serializer):
    action = serializers.CharField()
    line = serializers.CharField(required=False)
    from_line = serializers.CharField(required=False)
    to_line = serializers.CharField(required=False)
    at_station = serializers.CharField()


class PathResponseSerializer(serializers.Serializer):
    source = StationSerializer()
    destination = StationSerializer()
    path = StationSerializer(many=True)
    total_stations = serializers.IntegerField()
    total_distance_km = serializers.FloatField()
    total_time_minutes = serializers.IntegerField()
    fare_inr = serializers.IntegerField()
    steps = PathStepSerializer(many=True)
    optimized_for = serializers.CharField()
