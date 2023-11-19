import requests
import gzip
import json
from datetime import datetime    


def generate_elastic_query(condition, rules):
    # Build the Elasticsearch query based on the provided conditions
    # condition = query_json['condition']
    # rules = query_json['rules']
    logic = 'A'
    if condition == 'AND':
        query = {
                "bool": {
                        "must": [],
                }
        }
    else:
        logic = 'S'
        query = {
                "bool": {
                        "should": [],
                }
        }

    for rule in rules:
        cond = None
        clause = {}
        if 'condition' in rule:
            cond = rule['condition']
            clause = generate_elastic_query(cond, rule['rules'])
        else:   
          field = rule['field']
          operator = rule['operator']
          value = rule['value']
          if value == None:
              value = ''
          if field == "parentResourceId":
              field = "metadata."+field
          # Handle datetime type
          if rule['type'] == 'datetime':
              if type(value) == list:
                  for dtidx in range(len(value)):
                      value[dtidx] = datetime.strptime(value[dtidx], "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%SZ")
              elif value != '':
                ts = datetime.strptime(value, "%Y-%m-%d")
                value = ts.strftime("%Y-%m-%dT%H:%M:%SZ")
              # Assuming the date format is 'YYYY-MM-DD'
              #print(value)
              if rule['operator'] == 'equal':
                  clause = {
                      "bool": {
                          "must": [
                              {
                                  "term":{
                                      field: value
                                  }
                              }
                          ]
                          }
                      }
              
              if rule['operator'] == 'not_equal':
                  clause = {
                      "bool": {
                          "must_not": [
                              {
                                  "term":{
                                    field: value                                    
                                  }
                              }
                          ]
                          }
                      }
                  
              if rule['operator'] == 'less':
                  clause = {"bool": {
                          "must": [{
                      "range":{
                        field:{
                            "lt":value
                        }       
                      }
                  }]}}
              if rule['operator'] == 'less_or_equal':
                  clause = {"bool": {
                          "must": [{
                      "range":{
                        field:{
                            "lte":value
                        }       
                      }
                  }]}}
              if rule['operator'] == 'greater':
                  clause = {"bool": {
                          "must": [{
                      "range":{
                        field:{
                            "gt":value
                        }       
                      }
                  }]}}
              if rule['operator'] == 'greater_or_equal':
                  clause = {"bool": {
                          "must": [{
                      "range":{
                        field:{
                            "gte":value
                        }       
                      }
                  }]}}
              if rule['operator'] == 'between':
                  clause = {"bool": {
                          "must": [
                              {
                      "range":{
                        field:{
                            "gte":value[0],
                            "lte":value[1]
                        }       
                      }
                  }]
                  }
                  }
              if rule['operator'] == 'not_between':
                  clause = {"bool": {
                          "must_not": [
                              {
                      "range":{
                        field:{
                            "gte":value[0],
                            "lte":value[1]
                        }       
                      }
                  }]
                  }
                  }
              if rule['operator'] == 'is_null':
                  clause = {
                      "bool": {
                          "must_not": [
                              {
                                  "exists": {
                                    "field": field
                                  }
                              }
                          ]
                          }
                      }
              if rule['operator'] == 'is_not_null':
                  clause = {
                      "bool": {
                          "must": [
                              {
                                  "exists": {
                                    "field": field
                                  }
                              }
                          ]
                          }
                      }

                  
              
        
          if rule['type'] == 'string':
            field += '.keyword'
            if rule['operator'] == 'equal':
                  clause = {
                      "bool": {
                          "must": [
                              {
                                  "term":{
                                      field: value
                                  }
                              }
                          ]
                          }
                      }
            if rule['operator'] == 'not_equal':
                  clause = {
                      "bool": {
                          "must_not": [
                              {
                                  "term":{
                                      field: value
                                  }
                              }
                          ]
                          }
                      }
            if rule['operator'] == 'in' or rule['operator'] == 'contains': 
                  clause = {
                      "bool": {
                          "must": [
                              {
                                  "wildcard": {
                                  field: f"*{value}*"
                                }
                              }
                          ]
                          }
                      }
            if rule['operator'] == 'not_in' or rule['operator'] == 'not_contains':
                  clause = {
                      "bool": {
                          "must_not": [
                              {
                                  "wildcard": {
                                  field: f"*{value}*"
                                }
                              }
                          ]
                          }
                      }
            if rule['operator'] == 'begins_with':
                  clause = {
                      "bool": {
                          "must": [
                              {
                                  "wildcard": {
                                  field: f"{value}*"
                                }
                              }
                          ]
                          }
                      }
            if rule['operator'] == 'not_begins_with':
                  clause = {
                      "bool": {
                          "must_not": [
                              {
                                  "wildcard": {
                                  field: f"{value}*"
                                }
                              }
                          ]
                          }
                      }
            if rule['operator'] == 'ends_with':
                  clause = {
                      "bool": {
                          "must": [
                              {
                                  "wildcard": {
                                  field: f"*{value}"
                                }
                              }
                          ]
                          }
                      }
            if rule['operator'] == 'not_ends_with':
                  clause = {
                      "bool": {
                          "must_not": [
                              {
                                  "wildcard": {
                                  field: f"*{value}"
                                }
                              }
                          ]
                          }
                      }
            if rule['operator'] == 'is_null':
                  clause = {
                      "bool": {
                          "must_not": [
                              {
                                  "exists": {
                                    "field": field
                                  }
                              }
                          ]
                          }
                      }
            if rule['operator'] == 'is_not_null':
                  clause = {
                      "bool": {
                          "must": [
                              {
                                  "exists": {
                                    "field": field
                                  }
                              }
                          ]
                          }
                      }
            if rule['operator'] == 'is_empty':
                  clause = {
                      "bool": {
                          "must": [
                              {
                                  "term":{
                                      field: value
                                  }
                              }
                          ]
                          }
                      }
            if rule['operator'] == 'is_not_empty':
                  clause = {
                      "bool": {
                          "must_not": [
                              {
                                  "term":{
                                      field: value
                                  }
                              }
                          ]
                          }
                      }
           
        if logic == 'A':
            query["bool"]["must"].append(clause)
        else:
            query["bool"]["should"].append(clause)

    return query


# def get_query_response(condition, rules):
#     # Build the Elasticsearch query based on the provided conditions
#     if condition == 'AND':
#         query = {
#                 "bool": {
#                         "must": [],
#                 }
#         }
#     else:
#         query = {
#                 "bool": {
#                         "should": [],
#                 }
#         }

#     for rule in rules:
#         field = rule['field']
#         operator = rule['operator']
#         value = rule['value']

#         # Handle datetime type
#         if rule['type'] == 'datetime':
#             ts = datetime.strptime(value, "%Y-%m-%d")
#             ts.strftime("%Y-%m-%dT%H:%M:%SZ")
#             value = ts  # Assuming the date format is 'YYYY-MM-DD'
            
#             if rule['operator'] == 'equal':
#                 clause = {
#                     "match": {
#                         field: {
#                             "query": value,
#                             "operator": operator
#                         }
#                     }
#                 }
            
#             if rule['operator'] == 'not_equal':
#                 pass
#         # Create a query clause for each rule
#         # clause = {
#         #     "match": {
#         #         field: {
#         #             "query": value,
#         #             "operator": operator
#         #         }
#         #     }
#         # }

#         query["query"]["bool"]["must"].append(clause)

#     return query

def esqbuild(query):
    query_json = {"query": {}}
    query_json['query'] = generate_elastic_query(query['condition'], query['rules'])
    #print(query_json)

    base_url = 'https://search-jonathanlogs-tfvc4bowafzvwyzjiscandotga.aos.eu-north-1.on.aws/_search' # The domain with https:// and a trailing slash. For example, https://my-test-domain.us-east-1.es.amazonaws.com/
    auth = ('aizensosuke', 'Aizen_goat1311') # For testing only. Don't store credentials in code.

    headers = {'Accept-Encoding': 'gzip', 'Content-Type': 'application/json',
            'Content-Encoding': 'gzip'}
    

    # Compress the document.
    compressed_document = gzip.compress(json.dumps(query_json).encode())
    #print('in esqbuild----')
    # Send the request. 
    response = requests.get(base_url, auth=auth, headers=headers, data=compressed_document)
    #print(response.status_code)
    return response.json()

if __name__ == "__main__":
    q = {"query":{'bool': {'must': [{'bool': {'must': [{'term': {'resourceId.keyword': 'server-1234'}}]}}, {'bool': {'must': [{'bool': {'must': [{'range': {'timestamp': {'lte': '2023-11-15T00:00:00Z'}}}]}}]}}]}}}
    j = {
  "condition": "AND",
  "rules": [
    {
      "id": "name",
      "field": "resourceId",
      "type": "string",
      "input": "text",
      "operator": "begins_with",
      "value": "server"
    }
  ],
  "valid": True
}
    a = esqbuild(j)
    print(a)
    # print(a.status_code)
    # print(a.json())