from typing import Any, List, Dict

class ListResponse():
    def __init__(self, resources):
        self.list_response = create_base_list_response(resources)
    
def create_base_list_response(resources: List[Any]) -> Dict[Any]:
    list_response = {
        "schemas": [
            "urn:ietf:params:scim:api:messages:2.0:ListResponse"
        ],
        "totalResults": len(resources),
        "Resources": resources,
    }
    return list_response
