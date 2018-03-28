# pylint: disable=too-many-return-statements
import re
from elasticsearch_dsl import Q
from six import string_types


class RPNException(Exception):
    pass


def in_operator(field, value):
    if field == 'location.id':
        return in_operator_for_location(field, value)

    if value == [None]:
        return Q('missing', field=field)
    elif None in value:
        return Q(
            Q('terms', **{
                field + '.raw': [item for item in value if item is not None]
            }) |
            Q('missing', field=field),
        )
    else:
        return Q('terms', **{field + '.raw': value})


def in_operator_for_location(field, value):
    hidden_field = field.replace('.id', '.is_hidden')

    if value == [None]:
        return Q('missing', field=field)
    elif value == ["hidden"]:
        return Q('term', **{hidden_field: "true"})
    elif {None, "hidden"} == set(value):
        return Q(
            Q('missing', field=field) |
            Q('term', **{hidden_field: "true"}),
        )

    clean_items = [item for item in value if item not in [None, "hidden"]]

    if "hidden" not in value and None not in value:
        return Q(
            Q('terms', **{field + '.raw': clean_items}) &
            Q('term', **{hidden_field: "false"})
        )
    elif "hidden" in value and None not in value:
        return Q(
            Q('terms', **{field + '.raw': clean_items}) |
            Q('term', **{hidden_field: "true"})
        )
    elif "hidden" not in value and None in value:
        return Q(
            Q(
                Q('term', **{hidden_field: "false"}) &
                Q('terms', **{field + '.raw': clean_items})
            ) |
            Q('missing', field=field)
        )
    else:
        return Q(
            Q('missing', field=field) |
            Q('terms', **{field + '.raw': clean_items}) |
            Q('term', **{hidden_field: "true"})
        )


HI_OPERATORS = {
    '&&': lambda f1, f2: Q(f1 & f2),
    '||': lambda f1, f2: Q(f1 | f2),
}

LO_OPERATORS = {
    # requires multifield index, with raw being "not_analyzed"
    '=': lambda field, value: (
        Q('term', **{field: value}) if value is not None else
        Q('missing', field=field)
    ),
    '!=': lambda field, value: (
        Q(~Q('term', **{field: value})) if value is not None else
        Q('exists', field=field)
    ),

    # should those use .raw fields or not
    '<': lambda field, value: Q('range', **{field: {'lt': value}}),
    '<=': lambda field, value: Q('range', **{field: {'lte': value}}),
    '>': lambda field, value: Q('range', **{field: {'gt': value}}),
    '>=': lambda field, value: Q('range', **{field: {'gte': value}}),

    # wildcards. Might be slow, maybe use nGram indexer instead
    '*.': lambda field, value: Q(
        Q(
            "wildcard",
            **{field: {'value': "{}*".format(value)}}
        )
    ),
    '.*': lambda field, value: Q(
        Q(
            "wildcard",
            **{field: {'value': "*{}".format(value)}}
        )
    ),
    # sort and lower cause case insensitive
    '%': lambda field, value: Q(
        Q(
            "wildcard",
            **{field: {'value': "*{}*".format(value).lower()}}
        )
    ),

    # value is a values_list
    'in': lambda field, value: Q('terms', **{field: value}),
    '!in': lambda field, value: Q(~Q('terms', **{field: value})),
}

LO_OPERATORS_WITH_RAW_FIELDS = {
    # requires multifield index, with raw being "not_analyzed"
    '=': lambda field, value: (
        Q('term', **{field + '.raw': value}) if value is not None else
        Q('missing', field=field + '.raw')
    ),
    '!=': lambda field, value: (
        Q(~Q('term', **{field + '.raw': value})) if value is not None else
        Q('exists', field=field + '.raw')
    ),

    # should those use .raw fields or not
    '<': lambda field, value: Q('range', **{field + '.raw': {'lt': value}}),
    '<=': lambda field, value: Q('range', **{field + '.raw': {'lte': value}}),
    '>': lambda field, value: Q('range', **{field + '.raw': {'gt': value}}),
    '>=': lambda field, value: Q('range', **{field + '.raw': {'gte': value}}),

    # wildcards. Might be slow, maybe use nGram indexer instead
    '*.': lambda field, value: Q(
        Q(
            "wildcard",
            **{field + '.raw': {'value': "{}*".format(value)}}
        )
    ),
    '.*': lambda field, value: Q(
        Q(
            "wildcard",
            **{field + '.raw': {'value': "*{}".format(value)}}
        )
    ),
    # sort and lower cause case insensitive
    '%': lambda field, value: Q(
        Q(
            "wildcard",
            **{field + '.sort': {'value': "*{}*".format(value).lower()}}
        )
    ),

    # value is a values_list
    'in': in_operator,
    '!in': lambda field, value: Q(~in_operator(field, value)),
}


def parse_filter(token):
    if not isinstance(token, list) or len(token) != 3:
        raise RPNException("Wrong RPN: {}".format(token))

    field, low_op, _ = token
    if not re.search(r"^([.\w]+)$", field):
        raise RPNException("Wrong RPN: {}".format(token))

    if not isinstance(low_op, string_types) or low_op not in LO_OPERATORS.keys():
        raise RPNException("Wrong RPN: {}".format(token))

    return token


def is_list(data):
    if isinstance(data, list):
        return True

    return False


def to_list(value, converter=None):
    if converter:
        return [converter(v) for v in value]
    else:
        return value


def validate_filter(operator):
    if operator not in LO_OPERATORS.keys():
        raise RPNException("Wrong filter {}".format(operator))
    return True
