from collections import defaultdict
from celery.task import task
from alesya.models import Tag, Entity, ServiceTagBinding, Location, \
    LocationBinding


@task
def find_and_update_location_tags():
    location_entity = Entity.objects.get_or_create(
        name="Location"
    )
    Tag.objects.filter(name__startswith='г. ').update(entity_id=location_entity[0].id)
    Tag.objects.filter(name__startswith='г.п. ').update(entity_id=location_entity[0].id)
    Tag.objects.filter(name__endswith=' обл.').update(entity_id=location_entity[0].id)
    Tag.objects.filter(name__endswith=' область').update(entity_id=location_entity[0].id)
    Tag.objects.filter(name__endswith=' с/с').update(entity_id=location_entity[0].id)
    Tag.objects.filter(name__endswith=' р-н').update(entity_id=location_entity[0].id)


@task
def find_and_create_locations():
    location_entity = Entity.objects.get_or_create(
        name="Location"
    )
    tags = ServiceTagBinding.objects.filter(
        tag__entity_id=location_entity[0].id,
    ).order_by(
        "service_id", "-priority_order"
    ).values_list(
        "service_id", "tag__name"
    ).all()
    locations = []
    used_locations = dict(
        Location.objects.filter(
            name__in=[tag_name for _, tag_name in tags]
        ).values_list("name", "id").all()
    )
    used_location_names = set(used_locations.keys())
    for service_id, tag_name in tags:
        if tag_name in used_location_names:
            continue
        location = Location(
            name=tag_name,
        )
        locations.append(location)
        used_location_names.add(tag_name)
    Location.objects.bulk_create(locations)
    location_name_id_map = {location.name: location.id for location in locations}
    location_name_id_map.update(used_locations)
    service_tags_map = defaultdict(list)
    for service_id, tag_name in tags:
        service_tags_map[service_id].append(tag_name)
    bindings = []
    for service_id, tag_list in service_tags_map.items():
        parent_id = None
        for tag_name in tag_list:
            child_id = location_name_id_map[tag_name]
            if parent_id:
                bind = (parent_id, child_id)
                bindings.append(bind)
            parent_id = child_id
    bindings = list(dict.fromkeys(bindings))
    exists_bindings = LocationBinding.objects.values_list("parent_id", "child_id").all()
    bindings = [
        LocationBinding(parent_id=parent_id, child_id=child_id)
        for parent_id, child_id in bindings if (parent_id, child_id) not in exists_bindings
    ]
    LocationBinding.objects.bulk_create(bindings)
