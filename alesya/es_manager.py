from yrunner import wsgi
from elasticsearch.helpers import bulk

from alesya.models import Entity
from django.conf import settings

from elasticsearch_dsl import connections, Index, Search
from alesya.documents import EntityDocument


def drop_index():
    try:
        Index('entity').delete()
    except:
        pass


def create_index():
    EntityDocument.init()


def load_data():
    docs = []
    for entity in Entity.objects.all():
        entity_doc = EntityDocument(
            meta={'id': entity.id},
            name=entity.name,
            tags=entity.tags,
        )
        docs.append(entity_doc.to_dict(True))
    bulk(connections.get_connection(), docs)


def find_objects():
    connections.create_connection(**settings.ELASTICSEARCH_DSL.get('default'))
    connections.get_connection("default")
    search_query = Search()
    search_query = search_query.index("entity")
    search_query = search_query.doc_type(EntityDocument)
    search_query = search_query.query('match', name='velcom')
    for item in search_query.execute().hits:
        print(item.to_dict())
    pass


if __name__ == '__main__':
    # drop_index()
    # create_index()
    # load_data()
    find_objects()
