from django.test import TestCase
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Index, Search, A, Q
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.search import scan
from alesya import models as mx
from alesya.documents import EntityDocument
from django.conf import settings

from alesya.finder import Finder

INDEX_NAME = 'entity'


class FinderTest(TestCase):

    def tearDown(self):
        Index(INDEX_NAME).delete()

    def setUp(self):
        self.conn = connections.create_connection(**settings.ELASTICSEARCH_DSL.get('default'))

        try:
            Index(INDEX_NAME).delete()
        except Exception:
            pass
        EntityDocument.init()

    def install_data(self):
        companies = [
            mx.Company(name="ByFly"),
            mx.Company(name="МТС"),
            mx.Company(name="Velcom"),
            mx.Company(name="Unet"),
            mx.Company(name="Flowers City"),
            mx.Company(name="МТС Россия"),
        ]
        mx.Company.objects.bulk_create(companies)
        byfly = companies[0]
        mts = companies[1]
        velcom = companies[2]
        unet = companies[3]
        flowers_city = companies[4]
        mts_russia = companies[5]

        entities = {
            101: mx.Entity(number=101, name="МТТС: byfly, ZALA, Максифон", company_id=byfly.id),
            102: mx.Entity(number=102, name="Byfly,ZALA,Максифон,Умный дом", company_id=byfly.id),
            103: mx.Entity(number=103, name="Byfly,ZALA,Максифон,Умный дом", company_id=byfly.id),
            104: mx.Entity(number=104, name="Byfly,ZALA,Максифон,Умный дом", company_id=byfly.id),
            105: mx.Entity(number=105, name="Byfly,ZALA,Максифон,Умный дом", company_id=byfly.id),
            106: mx.Entity(number=106, name="Byfly,ZALA,Максифон,Умный дом", company_id=byfly.id),
            107: mx.Entity(number=107, name="Byfly,ZALA,Максифон,Умный дом", company_id=byfly.id),

            201: mx.Entity(number=201, name="МТС по N телефона", company_id=mts.id),
            202: mx.Entity(number=202, name="МТС по л/счету", company_id=mts.id),
            203: mx.Entity(number=203, name="Интернет", company_id=mts.id),

            301: mx.Entity(number=301, name="Абонентская плата за ТВ", company_id=velcom.id),
            302: mx.Entity(number=302, name="Абонентская плата за ТВ", company_id=velcom.id),
            303: mx.Entity(number=303, name="Цифровое ТВ Витязь", company_id=velcom.id),
            304: mx.Entity(number=304, name="velcom - по № телефона", company_id=velcom.id),
            305: mx.Entity(number=305, name="velcom - по л/счету", company_id=velcom.id),
            306: mx.Entity(number=306, name="v-кошелек", company_id=velcom.id),
            307: mx.Entity(number=307, name="Интернет, ТВ", company_id=velcom.id),
            308: mx.Entity(number=308, name="Интернет, ТВ", company_id=velcom.id),
            309: mx.Entity(number=309, name="Интернет, Комфорт ТВ", company_id=velcom.id),
            310: mx.Entity(number=310, name="Кабельное ТВ", company_id=velcom.id),

            401: mx.Entity(number=401, name="Интернет", company_id=unet.id),

            501: mx.Entity(number=501, name="Flowers-city.by", company_id=flowers_city.id),
            601: mx.Entity(number=601, name="МТС Россия", company_id=mts_russia.id),
        }
        mx.Entity.objects.bulk_create(entities.values())
        self.entity_ids = [entity.id for entity in entities.values()]
        classifiers = [
            mx.Сlassifier(
                name="Location", belong_to_class_question=None,
                question="Назовите город или населённый пункт"
            ),
        ]
        location = classifiers[0]
        mx.Сlassifier.objects.bulk_create(classifiers)
        classifier_tags = {
            2: mx.ClassifierTag(name="Минская область", classifier_id=location.id),
            3: mx.ClassifierTag(name="брест и брестская область", classifier_id=location.id),
            4: mx.ClassifierTag(name="могилев и могилевская область", classifier_id=location.id),
            5: mx.ClassifierTag(name="витебск и витебская область", classifier_id=location.id),
            6: mx.ClassifierTag(name="минск", classifier_id=location.id),
            7: mx.ClassifierTag(name="гомель и гомельская область", classifier_id=location.id),
            8: mx.ClassifierTag(name="гродно и гродненская область", classifier_id=location.id),
        }
        mx.ClassifierTag.objects.bulk_create(classifier_tags.values())
        
        classifier_tags_bindings = [
            mx.EntityClassifierTagBinding(
                entity=entities.get(101),
                classifier_tag=classifier_tags.get(2),
                priority_order=2,
            ),

            mx.EntityClassifierTagBinding(
                entity=entities.get(102),
                classifier_tag=classifier_tags.get(3),
                priority_order=2,
            ),

            mx.EntityClassifierTagBinding(
                entity=entities.get(103),
                classifier_tag=classifier_tags.get(4),
                priority_order=2,
            ),

            mx.EntityClassifierTagBinding(
                entity=entities.get(104),
                classifier_tag=classifier_tags.get(5),
                priority_order=2,
            ),

            mx.EntityClassifierTagBinding(
                entity=entities.get(105),
                classifier_tag=classifier_tags.get(6),
                priority_order=2,
            ),

            mx.EntityClassifierTagBinding(
                entity=entities.get(106),
                classifier_tag=classifier_tags.get(7),
                priority_order=2,
            ),

            mx.EntityClassifierTagBinding(
                entity=entities.get(107),
                classifier_tag=classifier_tags.get(8),
                priority_order=2,
            ),


            mx.EntityClassifierTagBinding(
                entity=entities.get(401),
                classifier_tag=classifier_tags.get(6),
                priority_order=2,
            ),
        ]
        mx.EntityClassifierTagBinding.objects.bulk_create(classifier_tags_bindings)

        tags = {
            1: mx.Tag(name="белтелеком"),
            9: mx.Tag(name="мобильная связь"),
            10: mx.Tag(name="мтс"),
            11: mx.Tag(name="интернет, телевидение"),
            12: mx.Tag(name="мтс - домашний интернет"),

            13: mx.Tag(name="velcom - voka"),
            14: mx.Tag(name="velcom - телесеть"),
            15: mx.Tag(name="velcom - гарант гомель"),
            16: mx.Tag(name="velcom"),
            17: mx.Tag(name="velcom - атлант телеком"),
            18: mx.Tag(name="терранэт - unet.by"),
            19: mx.Tag(name="зарубежные операторы"),
            20: mx.Tag(name="интернет-магазины"),
            21: mx.Tag(name="цветы"),
        }
        mx.Tag.objects.bulk_create(tags.values())

        tag_bindings = [
            mx.EntityTagBinding(
                entity=entities.get(101),
                tag=tags.get(1),
                priority_order=1,
            ),

            mx.EntityTagBinding(
                entity=entities.get(102),
                tag=tags.get(1),
                priority_order=1,
            ),

            mx.EntityTagBinding(
                entity=entities.get(103),
                tag=tags.get(1),
                priority_order=1,
            ),

            mx.EntityTagBinding(
                entity=entities.get(104),
                tag=tags.get(1),
                priority_order=1,
            ),

            mx.EntityTagBinding(
                entity=entities.get(105),
                tag=tags.get(1),
                priority_order=1,
            ),

            mx.EntityTagBinding(
                entity=entities.get(106),
                tag=tags.get(1),
                priority_order=1,
            ),

            mx.EntityTagBinding(
                entity=entities.get(107),
                tag=tags.get(1),
                priority_order=1,
            ),

            mx.EntityTagBinding(
                entity=entities.get(201),
                tag=tags.get(9),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(201),
                tag=tags.get(10),
                priority_order=2,
            ),

            mx.EntityTagBinding(
                entity=entities.get(202),
                tag=tags.get(9),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(202),
                tag=tags.get(10),
                priority_order=2,
            ),

            mx.EntityTagBinding(
                entity=entities.get(203),
                tag=tags.get(11),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(203),
                tag=tags.get(12),
                priority_order=2,
            ),

            mx.EntityTagBinding(
                entity=entities.get(301),
                tag=tags.get(11),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(301),
                tag=tags.get(13),
                priority_order=2,
            ),

            mx.EntityTagBinding(
                entity=entities.get(302),
                tag=tags.get(11),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(302),
                tag=tags.get(14),
                priority_order=2,
            ),

            mx.EntityTagBinding(
                entity=entities.get(303),
                tag=tags.get(11),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(303),
                tag=tags.get(15),
                priority_order=2,
            ),

            mx.EntityTagBinding(
                entity=entities.get(304),
                tag=tags.get(9),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(304),
                tag=tags.get(16),
                priority_order=2,
            ),

            mx.EntityTagBinding(
                entity=entities.get(305),
                tag=tags.get(9),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(305),
                tag=tags.get(16),
                priority_order=2,
            ),

            mx.EntityTagBinding(
                entity=entities.get(306),
                tag=tags.get(9),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(306),
                tag=tags.get(16),
                priority_order=2,
            ),

            mx.EntityTagBinding(
                entity=entities.get(307),
                tag=tags.get(11),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(307),
                tag=tags.get(17),
                priority_order=2,
            ),

            mx.EntityTagBinding(
                entity=entities.get(308),
                tag=tags.get(11),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(308),
                tag=tags.get(15),
                priority_order=2,
            ),

            mx.EntityTagBinding(
                entity=entities.get(309),
                tag=tags.get(11),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(309),
                tag=tags.get(15),
                priority_order=2,
            ),

            mx.EntityTagBinding(
                entity=entities.get(310),
                tag=tags.get(11),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(310),
                tag=tags.get(15),
                priority_order=2,
            ),

            mx.EntityTagBinding(
                entity=entities.get(401),
                tag=tags.get(11),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(401),
                tag=tags.get(18),
                priority_order=2,
            ),


            mx.EntityTagBinding(
                entity=entities.get(501),
                tag=tags.get(20),
                priority_order=1,
            ),
            mx.EntityTagBinding(
                entity=entities.get(501),
                tag=tags.get(21),
                priority_order=2,
            ),
        ]
        mx.EntityTagBinding.objects.bulk_create(tag_bindings)

    def add_data_to_es(self):
        docs = []
        for entity in mx.Entity.objects.all():
            entity_doc = EntityDocument.get_document(entity)
            data = entity_doc.to_dict(True)
            docs.append(data)
        bulk(connections.get_connection(), docs, refresh=True)

    def test_find_company(self):
        self.install_data()
        self.add_data_to_es()
        finder = Finder()
        name = 'интернет'
        result = finder.search(name)
        tag = result.get("tags")[0].get('key')
        result = finder.search_by_tags(tag)
        tag = result.get("tags")[1].get('key')
        result = finder.search_by_tags(tag)
