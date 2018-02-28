from django.db import models


class Service(models.Model):

    number = models.IntegerField(
        verbose_name="Service Number",
        unique=True,
    )
    name = models.CharField(
        verbose_name="Service name",
        max_length=100,
    )
    project_id = models.IntegerField(
        verbose_name="Project number",
        null=True,
        blank=True
    )

    def __str__(self):
        return "{name} | {number}".format(name=self.name, number=self.number)


class Entity(models.Model):

    name = models.CharField(
        verbose_name="Class name",
        max_length=100,
        unique=True,
    )
    belong_to_class_question = models.TextField(
        verbose_name="The question of belonging to a class",
        null=True,
        blank=True,
    )
    question = models.TextField(
        verbose_name="Class question",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(
        verbose_name="Name",
        max_length=100,
        unique=True,
    )
    entity = models.ForeignKey(
        Entity,
        null=True,
        blank=True,
        related_name="tags",
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name


class ServiceTagBinding(models.Model):

    class Meta:
        unique_together = ('service', 'tag', )

    service = models.ForeignKey(
        Service,
        related_name="tags_binding",
    )
    tag = models.ForeignKey(
        Tag,
        related_name="services_binding"
    )
    priority_order = models.IntegerField(
        verbose_name="Priority Order"
    )

    def __str__(self):
        return self.tag.name


class Location(models.Model):

    name = models.CharField(
        unique=True,
        max_length=100,
    )

    def __str__(self):
        return self.name


class LocationBinding(models.Model):

    class Meta:
        unique_together = (('child', 'parent',))

    child = models.ForeignKey(
        'Location',
        verbose_name="Child",
        related_name="parents",
    )
    parent = models.ForeignKey(
        'Location',
        verbose_name="Parent",
        related_name="children",
    )
