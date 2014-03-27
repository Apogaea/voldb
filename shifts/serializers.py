from rest_framework import serializers

from shifts.models import Shift


class ShiftSerializer(serializers.ModelSerializer):
    custom_error_messages = {
        'suspicious_owner': 'You cannot claim a shift for another user',
        'already_claimed': 'This shift has already been claimed',
        'unable_to_release': 'You may not release a shift cliamed by another user',
        'invalid_code': 'The code you submitted is invalid',
    }
    display_text = serializers.CharField(source='__str__', read_only=True)
    verification_code = serializers.CharField(required=False, write_only=True)
    requires_code = serializers.BooleanField(source='requires_code', read_only=True)

    class Meta:
        model = Shift
        fields = (
            'id', 'owner', 'display_text', 'verification_code',
            'requires_code',
        )

    def validate(self, attrs):
        if self.object.requires_code() and self.object.owner is None:
            submitted_code = attrs.get('verification_code')
            if not submitted_code == self.object.code:
                raise serializers.ValidationError(
                    self.custom_error_messages['invalid_code'],
                )
        return attrs

    def validate_owner(self, attrs, source):
        request = self.context['request']
        owner = attrs[source]
        if owner:
            if not owner == request.user:
                raise serializers.ValidationError(
                    self.custom_error_messages['suspicious_owner'],
                )
            elif self.object.owner:
                raise serializers.ValidationError(
                    self.custom_error_messages['already_claimed'],
                )
        elif self.object.owner:
            if not self.object.owner == request.user:
                raise serializers.ValidationError(
                    self.custom_error_messages['unable_to_release'],
                )

        return attrs
