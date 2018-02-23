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
        related_name="tags"
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
