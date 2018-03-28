from django.db import models


class Company(models.Model):

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    name = models.CharField(
        verbose_name="Service name",
        max_length=100,
    )


class Entity(models.Model):

    class Meta:
        verbose_name = 'Entity'
        verbose_name_plural = 'Entities'

    company = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        related_name="entities",
        on_delete=models.SET_NULL,
    )

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

    @property
    def tags(self):
        return list(EntityTagBinding.objects.filter(
            entity_id=self.id
        ).values_list("tag__name", flat=True).all())

    def __str__(self):
        return "{name} | {number}".format(name=self.name, number=self.number)


class Сlassifier(models.Model):

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


class ClassifierTag(models.Model):

    classifier = models.ForeignKey(
        Сlassifier,
        verbose_name="Classifier",
        null=True,
        blank=True,
    )
    name = models.CharField(
        verbose_name="Class item name",
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name


class EntityClassifierTagBinding(models.Model):

    class Meta:
        unique_together = ('entity', 'classifier_tag', )

    entity = models.ForeignKey(
        Entity,
        related_name="classifier_tags_binding",
    )
    classifier_tag = models.ForeignKey(
        ClassifierTag,
        related_name="entities_binding"
    )
    priority_order = models.IntegerField(
        verbose_name="Priority Order"
    )

    def __str__(self):
        return self.tag.name


class Tag(models.Model):

    name = models.CharField(
        verbose_name="Name",
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name


class EntityTagBinding(models.Model):

    class Meta:
        unique_together = ('entity', 'tag', )

    entity = models.ForeignKey(
        Entity,
        related_name="tags_binding",
    )
    tag = models.ForeignKey(
        Tag,
        related_name="entities_binding"
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
