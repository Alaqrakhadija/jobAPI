from rest_framework import serializers
from rest_framework.reverse import reverse

from job.models import Position, User


class PositionHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'position_detail'
    queryset = Position.objects.all()

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'pk': obj.company.pk,
            'pk2': obj.pk

        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class PositionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    company = serializers.ReadOnlyField(source='company.id')
    title = serializers.CharField(required=True, allow_blank=True, max_length=100)
    description = serializers.CharField(required=True, max_length=1000)
    apply_link = serializers.URLField()
    final_apply_date = serializers.DateField()

    def create(self, validated_data):
        return Position.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.apply_link = validated_data.get('apply_link', instance.apply_link)
        instance.final_apply_date = validated_data.get('final_apply_date', instance.final_apply_date)
        instance.save()
        return instance


class UserSerializer(serializers.HyperlinkedModelSerializer):
    positions = PositionHyperlink(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'address', 'phone_number', 'type', 'positions']

    # def get_fields(self, *args, **kwargs):
    #     fields = super().get_fields(*args, **kwargs)
    #     user = self.context.get('request').user
    #     # Check if the user is a company
    #     if self.instance.type == Type.COMPANY:
    #
    #         fields['position'] = serializers.HyperlinkedRelatedField(many=True, read_only=True,
    #                                                                  view_name='position-detail')
    #
    #     return fields


class ChatGPTSerializer(serializers.HyperlinkedModelSerializer):
    positions = PositionHyperlink(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'address', 'phone_number', 'type', 'positions']
