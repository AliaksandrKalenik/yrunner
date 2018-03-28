import uuid

from elasticsearch_dsl import Search, Q

from alesya.documents import EntityDocument


class Finder(object):

    def __init__(self):
        self.uuid = uuid.uuid4()
        self.find_phrases = []
        self.hits = None
        self.entity_ids = None

    def search(self, input):
        self.find_phrases.append(input)
        search_query = Search(doc_type=EntityDocument)
        search_query = search_query.post_filter('match', name=input)
        search_query.aggs.bucket('tags_agg', 'filters', filters={
            'tags_filter': Q('match', tags=input)
        })
        search_query.aggs['tags_agg'].bucket('companies', 'nested', path="company")
        search_query.aggs['tags_agg'].bucket('classificators-nested', 'nested', path='classificators')
        search_query.aggs['tags_agg']['classificators-nested'].bucket('classificators_agg', 'terms', field='classificators.entity_name.raw').bucket('classificators_tags_aggs', 'terms', field='classificators.name.raw')
        search_query.aggs['tags_agg'].bucket('tags_agg', 'terms', field='tags.raw')
        search_query.aggs['tags_agg']['companies'].bucket('companies_agg', 'terms', field='company.name.raw')
        search_query.aggs.bucket('name_agg', 'filters', filters={
            'name_filter': Q('match', name=input)
        })
        search_query.aggs['name_agg'].bucket('companies', 'nested', path="company")
        search_query.aggs['name_agg'].bucket('classificators-nested', 'nested', path='classificators')
        search_query.aggs['name_agg']['classificators-nested'].bucket('classificators_agg', 'terms', field='classificators.entity_name.raw').bucket('classificators_tags_aggs', 'terms', field='classificators.name.raw')

        search_query.aggs['name_agg']['companies'].bucket('companies_agg', 'terms', field='company.name.raw')
        search_query.aggs['name_agg']['companies']['companies_agg'].bucket('reverse-to-root', "reverse_nested")
        search_query.aggs['name_agg']['companies']['companies_agg']['reverse-to-root'].bucket('name_agg', 'terms', field='name.raw')
        self.entity_ids = []
        hits = []
        result = search_query.execute()
        for item in result.hits:
            self.entity_ids.append(item._id)
            hit = {
                "name": item.name,
                "company_name": item.company.name,
            }
            hits.append(hit)
        tags = [item.to_dict() for item in result.aggs['tags_agg']['buckets']['tags_filter']['tags_agg']['buckets']]
        return {
            "tags": tags,
            "hits": hits,
        }

    def search_by_tags(self, tag):
        if not self.entity_ids:
            raise ValueError("Make search first!")
        self.find_phrases.append(tag)
        search_query = Search(doc_type=EntityDocument)
        search_query = search_query.query('ids', values=self.entity_ids)
        search_query = search_query.post_filter('term', **{'tags.raw': tag})
        search_query.aggs.bucket('tags_agg', 'filters', filters={
            'tags_filter': Q('term', **{'tags.raw': tag})
        })
        search_query.aggs['tags_agg'].bucket('companies', 'nested', path="company")
        search_query.aggs['tags_agg'].bucket('classificators-nested', 'nested', path='classificators')
        search_query.aggs['tags_agg']['classificators-nested'].bucket('classificators_agg', 'terms', field='classificators.entity_name.raw').bucket('classificators_tags_aggs', 'terms', field='classificators.name.raw')
        search_query.aggs['tags_agg'].bucket('tags_agg', 'terms', field='tags.raw')
        search_query.aggs['tags_agg']['companies'].bucket('companies_agg', 'terms', field='company.name.raw')
        search_query.aggs.bucket('name_agg', 'filters', filters={
            'name_filter': Q('term', **{'tags.raw': tag})
        })
        search_query.aggs['name_agg'].bucket('companies', 'nested', path="company")
        search_query.aggs['name_agg'].bucket('classificators-nested', 'nested', path='classificators')
        search_query.aggs['name_agg']['classificators-nested'].bucket('classificators_agg', 'terms', field='classificators.entity_name.raw').bucket('classificators_tags_aggs', 'terms', field='classificators.name.raw')

        search_query.aggs['name_agg']['companies'].bucket('companies_agg', 'terms', field='company.name.raw')
        search_query.aggs['name_agg']['companies']['companies_agg'].bucket('reverse-to-root', "reverse_nested")
        search_query.aggs['name_agg']['companies']['companies_agg']['reverse-to-root'].bucket('name_agg', 'terms', field='name.raw')
        result = search_query.execute()
        self.entity_ids = []
        hits = []
        for item in result.hits:
            self.entity_ids.append(item._id)
            hit = {
                "name": item.name,
                "company_name": item.company.name,
            }
            hits.append(hit)
        tags = [
            item.to_dict()
            for item in result.aggs['tags_agg']['buckets']['tags_filter']['tags_agg']['buckets']
            if item.key != tag
        ]
        return {
            "tags": tags,
            "hits": hits,
        }

    def clear(self):
        self.find_phrases = []
        self.hits = None
