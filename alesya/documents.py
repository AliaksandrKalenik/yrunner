from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, Field, \
    Nested, Object
from elasticsearch_dsl.document import InnerDoc

from alesya.models import Entity, EntityTagBinding, EntityClassifierTagBinding


class StringField(Field):
    def to_dict(self):
        return STRING_FIELD


STRING_FIELD = {
    "type": "int",
    "fields": {
        "raw": {
            "type": "string",
            "analyzer": "preserving"
        },
        "normal_search": {
            "type": "string",
            "analyzer": "default",
        },
        "raw_search": {
            "type": "string",
            "analyzer": "search_analyzer",
        },
        "sort": {
            "type": "string",
            "analyzer": "keylower",
        },
    }
}


class CompanyDocument(InnerDoc):
    id = Integer()
    name = Text(analyzer='snowball', fields={'raw': Keyword()})


class ClassificatorDocument(InnerDoc):
    name = Text(analyzer='snowball', fields={'raw': Keyword()})
    entity_name = Text(analyzer='snowball', fields={'raw': Keyword()})
    entity_belong_to_class_question = Text()
    entity_question = Text()


class EntityDocument(DocType):
    name = Text(analyzer='standard', fields={'raw': Keyword()})
    tags = Text(analyzer='standard', fields={'raw': Keyword()})
    company = Nested(CompanyDocument)
    classificators = Nested(ClassificatorDocument)

    class Meta:
        index = 'entity'

    @staticmethod
    def get_document(entity_obj, op_type='index'):
        classifier_tag_qs = EntityClassifierTagBinding.objects.filter(
            entity_id=entity_obj.id,
        ).values_list(
            "classifier_tag__classifier_id",
            "classifier_tag__name",
            "classifier_tag__classifier__name",
            "classifier_tag__classifier__belong_to_class_question",
            "classifier_tag__classifier__question",
        )
        class_docs = []
        for class_tag in classifier_tag_qs.all():
            tags_doc = ClassificatorDocument(
                meta={'id': class_tag[0]},
                name=class_tag[1],
                entity_name=class_tag[2],
                entity_entity_belong_to_class_question=class_tag[3],
                entity_question=class_tag[4],
            )
            class_docs.append(tags_doc)
        entity_doc = EntityDocument(
            meta={'id': entity_obj.id, '_op_type': op_type},
            name=entity_obj.name,
            tags=entity_obj.tags,
            classificators=class_docs
        )
        if entity_obj.company:
            company_doc = CompanyDocument(
                id=entity_obj.company_id,
                name=entity_obj.company.name,
            )
            entity_doc.company = company_doc
        return entity_doc
