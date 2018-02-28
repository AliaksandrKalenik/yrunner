from django.contrib import admin

from alesya.models import Service, Tag, ServiceTagBinding, Entity, Location, \
    LocationBinding
from alesya.tasks import find_and_update_location_tags, \
    find_and_create_locations


class TagInline(admin.TabularInline):
    model = ServiceTagBinding


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    search_fields = ('name', 'number', )

    def tags(self):
        limit = 10
        tags = list(
            Tag.objects.filter(
                services_binding__service_id=self.id
            ).order_by(
                'services_binding__priority_order'
            ).values_list(
                "name", flat=True
            ).all()[:limit]
        )
        tags_count = len(Tag.objects.filter(
            services_binding__service_id=self.id
        ))
        if tags_count > limit:
            tags.append("...")
        return tags

    tags.short_description = "Tags"

    list_display = ('id', 'name', 'number', tags)
    inlines = (TagInline,)


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "belong_to_class_question", "question")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name', )

    def path(self):
        if not self.entity:
            return ""
        if self.entity.name != "Location":
            return ""
        service_ids = ServiceTagBinding.objects.filter(tag_id=self.id).values_list("service_id", flat=True).all()
        tags = ServiceTagBinding.objects.filter(
            service_id__in=service_ids
        ).order_by(
            "service_id", "priority_order"
        ).values_list("service_id", "tag__name").all()
        from collections import defaultdict
        result = defaultdict(list)
        for tag in tags:
            result[tag[0]].append(tag[1])
        path_list = [", ".join(tags) for service_id, tags in result.items()]
        path_list = list(dict.fromkeys(path_list))
        result_str = "<br>".join(path_list)
        return result_str

    path.short_description = "Path"
    path.allow_tags = True

    list_display = ("id", "name", "entity", path, )

    def update_location_tags_action(self, request, queryset):
        find_and_update_location_tags.apply_async(retry=False)
        self.message_user(
            request, "Location tags updating started"
        )
    find_and_update_location_tags.short_description = "Update Location tags"

    def make_location_tree(self, request, queryset):
        find_and_create_locations.apply_async(retry=False)
        self.message_user(
            request, "Finding and creating locations started"
        )
    make_location_tree.short_description = "Find and create locations from tags"

    actions = (
        update_location_tags_action,
        make_location_tree,
    )


class ParentLocationBindingInline(admin.TabularInline):
    model = LocationBinding
    fk_name = 'parent'


class ChildLocationBindingInline(admin.TabularInline):
    model = LocationBinding
    fk_name = 'child'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    inlines = [ParentLocationBindingInline, ChildLocationBindingInline]

    def parents(self):
        parent_list = []

        def get_parents(location, current_path=None):
            if current_path is None:
                current_path = []
                parent_list.append(current_path)
            parent_locations = location.parents.all()
            current_path.append(location.name)
            paths = [current_path[:] for item in range(0, len(parent_locations) - 1 )]
            if len(paths) > 0:
                parent_list.extend(paths)
            paths.insert(0, current_path)
            for index, parent in enumerate(parent_locations):
                get_parents(parent.parent, paths[index])

        get_parents(self)
        return "<br>".join(["-->".join(path[::-1]) for path in parent_list])

    parents.short_description = "Parents"
    parents.allow_tags = True

    def children(self):
        child_list = []

        def get_children(location, current_path=None):
            if current_path is None:
                current_path = []
                child_list.append(current_path)
            child_locations = location.children.all()
            current_path.append(location.name)
            paths = [current_path[:] for item in range(0, len(child_locations) - 1 )]
            if len(paths) > 0:
                child_list.extend(paths)
            paths.insert(0, current_path)
            for index, parent in enumerate(child_locations):
                get_children(parent.child, paths[index])

        get_children(self)
        return "<br>".join(["-->".join(path) for path in child_list])

    children.short_description = "Childs"
    children.allow_tags = True

    list_display = ('id', 'name', parents, children)
