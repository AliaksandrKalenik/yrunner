from django.contrib import admin

from alesya.models import Service, Tag, ServiceTagBinding, Classification


class TagInline(admin.TabularInline):
    model = ServiceTagBinding


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

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
        print(tags)
        return tags

    tags.short_description = "Tags"

    list_display = ('id', 'name', 'number', tags)
    inlines = (TagInline,)


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "belong_to_class_question", "question")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "classification", )
