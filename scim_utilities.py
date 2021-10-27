from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Dict, Union
from warnings import warn


class ListResponse:
    def __init__(self, resources):
        self.list_response = create_base_list_response(resources)


def create_base_list_response(resources: List[Any]) -> Dict[Any]:
    list_response = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": len(resources),
        "Resources": resources,
    }
    return list_response


class AttributeType(Enum):
    """The schema attribute type"""

    STRING = "string"
    BOOLEAN = "boolean"
    DECIMAL = "decimal"
    INTEGER = "integer"
    DATE_TIME = "dateTime"
    REFERENCE = "reference"
    COMPLEX = "complex"


class Mutability(Enum):
    """The schema attribute mutability"""

    READ_ONLY = "readOnly"
    READ_WRITE = "readWrite"
    IMMUTABLE = "immutable"
    WRITE_ONLY = "writeOnly"


class Returned(Enum):
    """The schema attribute returned value"""

    ALWAYS = "always"
    NEVER = "never"
    DEFAULT = "default"
    REQUEST = "request"


class Uniqueness(Enum):
    NONE = "none"
    SERVER = "server"
    GLOBAL = "global"


class ReferenceTypes(Enum):
    # FIXME - This isn't right. Need to be able to house values
    USER = "User"
    GROUP = "Group"
    EXTERNAL = "external"
    URI = "uri"


class SCIMViolation(Exception):
    """Exception raised for a violation of the SCIM standard"""

    def __init__(self, message):
        self.message = message


class SchemaAttribute:
    """Defined in https://datatracker.ietf.org/doc/html/rfc7643#section-7"""

    def __init__(
        self,
        *,
        name: str,
        type: AttributeType,
        sub_attributes: List["SchemaAttribute"] = None,  # Only if "type" == "complex"
        multi_valued: bool,
        description: str,
        required: bool,
        canonical_values: None,
        case_exact=bool,
        mutability: Mutability,
        returned: Returned,
        uniqueness: Uniqueness,
        reference_types: ReferenceTypes,  # Only if "type" == "reference"
    ):

        self.name = name
        self.type = type
        self.sub_attributes = sub_attributes
        self.multi_valued = multi_valued
        self.description = description
        self.requred = required
        self.canonical_values = canonical_values
        self.case_exact = case_exact
        self.mutability = mutability
        self.returned = returned
        self.uniqueness = uniqueness
        self.reference_types = reference_types

        self._warn_on_complex_type_missing_sub_attributes()
        self._throw_exception_on_sub_attributes_but_not_complex_type()

    def _warn_on_complex_type_missing_sub_attributes(self):
        if self.attribute_type == AttributeType.COMPLEX and self.sub_attributes == None:
            warn(
                f'Attribute "{self.name}" has the type "complex", but is missing sub-attributes. This is recommended per RFC 7643 § 7.'
            )

    def _throw_exception_on_sub_attributes_but_not_complex_type(self):
        if self.attribute_type != AttributeType.COMPLEX and self.sub_attributes != None:
            raise SCIMViolation(
                f'Attribute "{self.name}" has sub-attributes, but is not of type "complex"'
            )


class Schema:
    """Defined in https://datatracker.ietf.org/doc/html/rfc7643#section-7"""

    _SCHEMA_ATTRIBUTES = [
        SchemaAttribute(
            name="id",
            type=AttributeType.STRING,
            multi_valued=False,
            description="The unique URI of the schema. When applicable, service providers MUST specify the URI.",
            required=True,
            case_exact=False,
            mutability=Mutability.READ_ONLY,
            returned=Returned.DEFAULT,
            uniqueness=Uniqueness.NONE,
        ),
        SchemaAttribute(
            name="name",
            type=AttributeType.STRING,
            multi_valued=False,
            description="The schema's human-readable name. When applicable, service providers MUST specify the name, e.g., 'User'.",
            required=True,
            case_exact=False,
            mutability=Mutability.READ_ONLY,
            returned=Returned.DEFAULT,
            uniqueness=Uniqueness.NONE,
        ),
        SchemaAttribute(
            name="description",
            type=AttributeType.STRING,
            multi_valued=False,
            description="The schema's human-readable description.",
            required=False,
            case_exact=False,
            mutability=Mutability.READ_ONLY,
            returned=Returned.DEFAULT,
            uniqueness=Uniqueness.NONE
        )
    ]

    def __init__(
        self,
        *,
        id: Union[int, str] = "urn:ietf:params:scim:schemas:core:2.0:Schema",
        name: str = "Schema",
        description: str = "Specifies the schema that describes a SCIM schema",
        attributes: List[SchemaAttribute] = _SCHEMA_ATTRIBUTES,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.attributes = attributes


class User(Schema):
    def __init__(
        self,
        *,
        user_name: str,
        formatted: str = None,
        family_name: str = None,
        given_name: str = None,
        middle_name: str = None,
        honorific_prefix: str = None,
        honorific_suffix: str = None,
        display_name: str = None,
        nick_name: str = None,
        profile_url: str = None,
        title: str = None,
        userType: str = None,
        preferred_language: str = None,
        locale: str = None,
        timezone: str = None,
        active: str = None,
        password: str = None,
        emails: List[str] = None,
        phone_numbers: List[str] = None,
        ims: List[str] = None,
        photos: List[str] = None,
    ):
        self.id = "urn:ietf:params:scim:schemas:core:2.0:User"
        self.name = "User"
        self.user_name = user_name
        self.description = "User Account"
        self.endpoint = "/Users"
