from hustings.models import Husting
from rest_framework import serializers


class HustingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Husting
        fields = (
            "title",
            "url",
            "starts",
            "ends",
            "location",
            "postevent_url",
        )
