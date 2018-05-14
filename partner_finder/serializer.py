from rest_framework import serializers
from partner_finder.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('organizer', 'activity', 'email', 
        	'start_time', 'end_time', 'post_time')
