# pylint: disable=too-many-locals
from collections import defaultdict

from elasticsearch_dsl import Q

from .rpn_helper import HI_OPERATORS, RPNException
from .rpn_helper import LO_OPERATORS
from .rpn_helper import LO_OPERATORS_WITH_RAW_FIELDS
from .rpn_helper import is_list
from .rpn_helper import parse_filter
from .rpn_helper import to_list
from .rpn_helper import validate_filter


# pylint: disable=too-many-arguments

class FilterManager(object):
    def __init__(self, resource_cls, nested_field_map=None, raw_fields=True):
        self.nested_field_map = nested_field_map or {}
        self.resource_cls = resource_cls
        if raw_fields:
            self.lo_operators = LO_OPERATORS_WITH_RAW_FIELDS
        else:
            self.lo_operators = LO_OPERATORS

    def create_filter(self, ids, query_list=None, filter_fields=None):
        """
        :param ids: resource identifiers
        :type ids: list[int|str]
        :param query_list: rpn query
        :type query_list: list[list|str]
        :param filter_fields: fields can present in filter
        :type filter_fields: list[str]
        :return: filter object
        :rtype: elasticsearch_dsl.Q
        """

        parsed_filters = self.get_es_query_from_query_list(
            query_list, filter_fields)
        final_filters = None
        if parsed_filters and ids:
            ids_filter = Q(
                "ids",
                values=ids,
                type=self.resource_cls._doc_type.index
            )
            assert len(parsed_filters) == 1  # got result
            result_filters = parsed_filters.pop()
            final_filters = HI_OPERATORS['&&'](ids_filter, result_filters)
        elif ids:
            ids_filter = Q(
                "ids",
                values=ids,
                type=self.resource_cls._doc_type.index
            )
            final_filters = ids_filter
        elif parsed_filters:
            assert len(parsed_filters) == 1  # got result
            final_filters = parsed_filters.pop()

        return final_filters

    def get_es_query_from_query_list(self, query_list, filter_fields):
        if not query_list:
            return None
        stack = []
        for item in query_list:
            if not isinstance(item, list) and item in HI_OPERATORS:
                self.parse_hi_operator(item, stack)
            else:
                self.parse_lo_operator(item, stack, filter_fields)

        return [item for item in stack if item]

    def parse_hi_operator(self, item, stack):
        hi_op = HI_OPERATORS[item]
        if len(stack) < 2:
            raise RPNException('RPN invalid. Operand missing')

        operand_a = stack.pop()
        operand_b = stack.pop()
        stack.append(self.hi_op_checking_placeholders(
            hi_op, operand_a, operand_b
        ))

    def parse_lo_operator(self, item, stack, filter_fields):
        field, low_op, value = parse_filter(item)
        field_name, _ = self.parse_field(field)
        if filter_fields is not None and field_name not in filter_fields:
            # inaccessible field, this filter should be ignored
            # put placeholder so hi operators don't break
            # and remove it later
            stack.append(None)
            return

        validate_filter(low_op)
        low_op_func = self.lo_operators[low_op]

        res = self.create_low_operation_filter(
            field=field,
            low_op=low_op,
            low_op_func=low_op_func,
            value=value
        )
        stack.append(res)

    def parse_field(self, field):
        """
        :param field: string field in filter
        :return: tuple (dict field name, inner field name)
        """
        field_tokens = field.split('.')
        if len(field_tokens) > 2:
            raise Exception(
                code='filter-field-incorrect',
                details='Filter is incorrect. Field can only have one dot in it'
            )
        resource_field = field_tokens[0]
        dict_field = field_tokens[1] if len(field_tokens) > 1 else None
        return resource_field, dict_field

    def create_low_operation_filter(self, field, low_op, low_op_func, value):

        # check value and perhaps convert it to
        # appropriate type of the field
        # get converter from resource

        # get related resource from field route
        # converter = related_resource.to_self_type

        # before, somehow check that field is not relation
        # then:
        field_name, _ = self.parse_field(field)

        # resource_field = getattr(self.resource_cls, field_name, None)
        # if not resource_field:
        #     raise BaseApiException(
        #         code='filter-field-incorrect',
        #         details='Filter is incorrect. {} has no attribute '
        #                 '{}'.format(self.resource_cls.__name__, field)
        #     )

        # value = self.convert_value(low_op, value, resource_field)
        # field = self.nested_field_map.get(field, field)
        res = low_op_func(field, value)
        return res

    def convert_value(self, low_op, value, resource_field):
        converter = self.get_converter(resource_field)
        if low_op in ['in', '!in']:
            if is_list(value):
                return to_list(value, converter)
            else:
                raise RPNException(
                    'RPN invalid. List value expected after'
                    ' "{}" operator.'.format(low_op)
                )
        elif converter:
            return converter(value)

    def get_converter(self, resource_field):
        # field_type = resource_field.Meta.value_type
        # if field_type in (int, float):
        #     return lambda i: field_type(i) if i else i
        #     # pylint: disable=cell-var-from-loop
        # else:
        return lambda i: i

    def hi_op_checking_placeholders(self, hi_op, operand_a, operand_b):
        if operand_a and operand_b:
            return hi_op(operand_b, operand_a)
        elif operand_a and not operand_b:
            return operand_a
        elif not operand_a and operand_b:
            return operand_b

    def get_exact_filtered_fields(self, query_list=None):
        rpn_query = query_list or []

        exact_filtered_fields = []
        for item in rpn_query:
            if isinstance(item, list):
                field, low_op, value = parse_filter(item)
                if low_op == '=' and value:
                    exact_filtered_fields.append(field)

        return exact_filtered_fields

    def create_filter_for_aggs(self, query_list=None, filter_fields=None):
        filters_list = self.get_lo_operation_filters_list(query_list)

        field_filter_map = defaultdict(list)
        for item in filters_list:
            # catch date and estimated_market_value fields here and use estimate
            # filter for them.
            field, low_op, value = parse_filter(item)
            field_name, _ = self.parse_field(field)
            if filter_fields is not None and field_name not in filter_fields:
                continue

            low_op_func = self.lo_operators[low_op]
            validate_filter(low_op)
            # TODO: this will break if filters have same filter for same field,
            # TODO: like  date <= 1 and date <= 2.
            res = self.create_low_operation_filter(
                field=field,
                low_op=low_op,
                low_op_func=low_op_func,
                value=value,
            )
            field_filter_map[field].append(res)

        return field_filter_map

    def get_lo_operation_filters_list(self, query_list):
        query_list = query_list or []
        if '||' in query_list:
            raise RPNException(
                'RPN invalid. Currently does not support || in filters for'
                ' aggregated queries.'
            )

        # validation of RPN
        filters = []
        stack_count = 0
        for item in query_list:
            if item == '&&':
                if stack_count < 2:
                    raise RPNException('RPN invalid. Operand missing')

                stack_count -= 1
            else:
                filters.append(item)
                stack_count += 1

        if query_list and stack_count != 1:
            raise RPNException('RPN invalid. Operand missing')
        return filters

    def create_filter_with_aggs(self, ids, query_list=None, filter_fields=None):
        filters_dict = self.create_filter_for_aggs(
            query_list=query_list,
            filter_fields=filter_fields
        )

        if ids:
            ids_filter = Q(
                "ids",
                values=ids,
                type=self.resource_cls._doc_type.index
            )
        if filters_dict:
            filters = [
                filter_
                for filters in filters_dict.values()
                for filter_ in filters
            ]
            if ids:
                filters.append(ids_filter)
            final_filters = Q('bool', must=filters)
        else:
            final_filters = ids_filter

        return final_filters
