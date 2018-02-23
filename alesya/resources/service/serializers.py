from rest_framework.fields import ListField, CharField
from rest_framework.serializers import ModelSerializer

from alesya.models import Service, Tag, ServiceTagBinding


class TagListField(ListField):

    child = CharField()

    def to_representation(self, obj):
        return list(
            Tag.objects.filter(
                services_binding__service_id=obj.id
            ).order_by(
                "services_binding__priority_order"
            ).values_list('name', flat=True).all()
        )

    def to_internal_value(self, data):
        return {}


class ServiceSerializer(ModelSerializer):

    tags = TagListField(source='*')

    class Meta:
        model = Service
        fields = ("id", "number", "name", "tags", )

    def create(self, validated_data):
        result = super(ServiceSerializer, self).create(validated_data)
        self.post_create(result)
        return result

    def update(self, instance, validated_data):
        result = super(ServiceSerializer, self).update(instance, validated_data)
        self.post_update(result)
        return result

    def post_update(self, obj):
        if 'tags' in self.initial_data:
            self.create_not_exists_tags()
            self.set_service_tags(obj)

    def post_create(self, obj):
        if 'tags' in self.initial_data:
            self.create_not_exists_tags()
            self.set_service_tags(obj)

    def is_valid(self, raise_exception=False):
        self.create_not_exists_tags()
        result = super(ServiceSerializer, self).is_valid(raise_exception)
        return result

    def create_not_exists_tags(self):
        initial_data = dict(self.initial_data)
        tags = initial_data.get('tags')
        if not tags:
            return
        exists_tags = Tag.objects.filter(
            name__in=tags
        ).values_list(
            "name", flat=True
        ).all()
        tags_to_create = []
        for tag_name in set(tags) - set(exists_tags):
            tag = Tag(name=tag_name)
            tags_to_create.append(tag)
        Tag.objects.bulk_create(tags_to_create)
        return True

    def set_service_tags(self, obj):
        ServiceTagBinding.objects.filter(service_id=obj.id).delete()
        initial_data = dict(self.initial_data)
        tags = initial_data.get('tags', [])
        tags = list(dict.fromkeys(tags))  # remove duplicates
        if not tags:
            return
        tag_id_map = dict(Tag.objects.filter(name__in=tags).values_list("name", "id").all())
        binds = []
        for priority_order, tag in enumerate(tags):
            bind = ServiceTagBinding(
                service_id=obj.id,
                tag_id=tag_id_map[tag],
                priority_order=priority_order
            )
            binds.append(bind)
        ServiceTagBinding.objects.bulk_create(binds)
