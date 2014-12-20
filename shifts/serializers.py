from django.conf import settings

from rest_framework import serializers

from shifts.models import Shift


class ShiftSerializer(serializers.ModelSerializer):
    custom_error_messages = {
        'suspicious_owner': 'You cannot claim a shift for another user',
        'already_claimed': 'This shift has already been claimed',
        'unable_to_release': 'You may not release a shift claimed by another user',
        'invalid_code': 'The code you submitted is invalid',
    }
    display_text = serializers.CharField(source='__unicode__', read_only=True)
    verification_code = serializers.CharField(required=False, write_only=True)
    requires_code = serializers.BooleanField(read_only=True)
    department = serializers.CharField(read_only=True)
    start = serializers.CharField(source='get_start_time_display', read_only=True)
    shift_length = serializers.IntegerField(read_only=True)

    class Meta:
        model = Shift
        fields = (
            'id', 'owner', 'display_text', 'verification_code',
            'requires_code', 'department', 'start', 'shift_length',
        )

    def validate(self, attrs):
        if not settings.REGISTRATION_OPEN:
            raise serializers.ValidationError('Registration closed')
        if self.instance.requires_code() and self.instance.owner is None:
            submitted_code = attrs.get('verification_code')
            if not submitted_code == self.instance.code:
                raise serializers.ValidationError(
                    self.custom_error_messages['invalid_code'],
                )
        return attrs

    def validate_owner(self, value):
        request = self.context['request']
        if value:
            if not value == request.user:
                raise serializers.ValidationError(
                    self.custom_error_messages['suspicious_owner'],
                )
            elif self.instance.owner:
                raise serializers.ValidationError(
                    self.custom_error_messages['already_claimed'],
                )
        elif self.instance.owner:
            if not self.instance.owner == request.user:
                raise serializers.ValidationError(
                    self.custom_error_messages['unable_to_release'],
                )

        return value
