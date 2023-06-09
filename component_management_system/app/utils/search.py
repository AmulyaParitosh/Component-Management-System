import re

from flask_sqlalchemy.query import Query


def search_query(model, model_attribute, search_str: str):

	tags: list[model] = model.query.filter(model_attribute.contains(search_str)).all()

	for word in search_str.split(" "):
		query:list[Query] = model.query.filter(model_attribute.contains(word)).all()
		tags.extend(q for q in query if q not in tags)

	return tags


def make_fuzzy_query(value: str):
    query = {
                "fuzzy" : {
                    "name": {
                        "value": value,
                        "fuzziness":"AUTO",
                        "transpositions":True,
                        "max_expansions": 100,
                        "boost": 5
                    }
                }
            }
    return query


def make_regexp_query(value: str):
    query = {
        "regexp": {
            "name": {
                "value" : value,
                "flags": "ALL",
                "case_insensitive": True,
            }
        }
    }
    return query


def make_must_query_list(search_key: str):
    value_list = re.split(r" |,|\||-|_|\.", search_key)
    query_list = []
    for value in value_list:
        query_list.append(make_fuzzy_query(value))
    return query_list


def make_should_query_list(search_key: str):
    value_list = re.split(r" |,|\||-|_|\.", search_key)
    query_list = []
    for value in value_list:
        query_list.append(make_fuzzy_query(value))
    for value in value_list:
        query_list.append(make_regexp_query(value))

    query_list.append(
        {
            "more_like_this" : {
                "fields" : ["name"],
                "like" : search_key,
                "min_term_freq" : 1,
                "max_query_terms" : 12
            }
        }
    )

    return query_list


def make_elasticsearch_query(search_key: str):
    query = {
        "bool": {
            # "must": make_must_query_list(search_key),
            "should": make_should_query_list(search_key),
        }
    }
    return query
