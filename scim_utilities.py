from abc import ABC, abstractmethod
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
    """Defined in https://datatracker.ietf.org/doc/html/rfc7643#section-7
    Default values defined in RFC 7643 § 2.2
    """

    def __init__(
        self,
        *,
        name: str,
        type: AttributeType = AttributeType.STRING,
        sub_attributes: List["SchemaAttribute"] = None,  # Only if "type" == "complex"
        multi_valued: bool,
        description: str,
        required: bool = False,
        canonical_values: List[str] = None,
        case_exact: bool = False,
        mutability: Mutability = Mutability.READ_WRITE,
        returned: Returned = Returned.DEFAULT,
        uniqueness: Uniqueness = Uniqueness.NONE,
        reference_types: ReferenceTypes = None,  # Only if "type" == "reference"
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
        if self.type == AttributeType.COMPLEX and self.sub_attributes == None:
            warn(
                f'Attribute "{self.name}" has the type "complex", but is missing sub-attributes. This is recommended per RFC 7643 § 7.'
            )

    def _throw_exception_on_sub_attributes_but_not_complex_type(self):
        if self.type != AttributeType.COMPLEX and self.sub_attributes != None:
            raise SCIMViolation(
                f'Attribute "{self.name}" has sub-attributes, but is not of type "complex"'
            )


class SCIMSchema(ABC):
    """An abstract representation of a SCIM schema. Not to be confused with the "Schema" resource."""

    def __init__(
        self, *, id: str, name: str, description: str, attributes: List[SchemaAttribute]
    ):
        self.id = id
        self.name = name
        self.description = description
        self.attributes = attributes

    @abstractmethod
    def dumps(self):
        """Returns a JSON-serializable representation of the schema."""
        pass


class Schema(SCIMSchema):
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
            description="The schema's human-readable description. When applicable, service providers MUST specify the description.",
            required=False,
            case_exact=False,
            mutability=Mutability.READ_ONLY,
            returned=Returned.DEFAULT,
            uniqueness=Uniqueness.NONE,
        ),
        SchemaAttribute(
            name="attributes",
            type=AttributeType.COMPLEX,
            multi_valued=True,
            description="A complex attribute that includes the attributes of a schema.",
            required=True,
            mutability=Mutability.READ_ONLY,
            returned=Returned.DEFAULT,
            uniqueness=Uniqueness.NONE,
            sub_attributes=[
                SchemaAttribute(
                    name="name",
                    type=AttributeType.STRING,
                    multi_valued=False,
                    description="The attribute's name.",
                    required=True,
                    case_exact=True,
                    mutability=Mutability.READ_ONLY,
                    returned=Returned.DEFAULT,
                    uniqueness=Uniqueness.NONE,
                ),
                SchemaAttribute(
                    name="type",
                    type=AttributeType.STRING,
                    multi_valued=False,
                    description="The attribute's data type. Valid values include 'string', 'complex', 'boolean', 'decimal', 'integer', 'dateTime', 'reference'.",
                    required=True,
                    canonical_values=[
                        "string",
                        "complex",
                        "boolean",
                        "decimal",
                        "integer",
                        "dateTime",
                        "reference",
                    ],
                    case_exact=False,
                    mutability=Mutability.READ_ONLY,
                    returned=Returned.DEFAULT,
                    uniqueness=Uniqueness.NONE,
                ),
                SchemaAttribute(
                    name="multiValued",
                    type=AttributeType.BOOLEAN,
                    multi_valued=False,
                    description="A Boolean value indicating an attribute's plurality.",
                    required=True,
                    mutability=Mutability.READ_ONLY,
                    returned=Returned.DEFAULT,
                    uniqueness=Uniqueness.NONE,
                ),
                SchemaAttribute(
                    name="description",
                    type=AttributeType.STRING,
                    multi_valued=False,
                    description="A human-readable description of the attribute.",
                    required=False,
                    case_exact=True,
                    mutability=Mutability.READ_ONLY,
                    returned=Returned.DEFAULT,
                    uniqueness=Uniqueness.NONE,
                ),
                SchemaAttribute(
                    name="required",
                    type=AttributeType.BOOLEAN,
                    multi_valued=False,
                    description="A boolean value indicating whether or not the attribute is required.",
                    required=False,
                    mutability=Mutability.READ_ONLY,
                    returned=Returned.DEFAULT,
                    uniqueness=Uniqueness.NONE,
                ),
                SchemaAttribute(
                    name="canonicalValues",
                    type=AttributeType.STRING,
                    multi_valued=True,
                    description="A collection of canonical values. When applicable, service providers MUST specify the canonical types, e.g., 'work', 'home'.",
                    required=False,
                    case_exact=True,
                    mutability=Mutability.READ_ONLY,
                    returned=Returned.DEFAULT,
                    uniqueness=Uniqueness.NONE,
                ),
                SchemaAttribute(
                    name="caseExact",
                    type=AttributeType.BOOLEAN,
                    multi_valued=False,
                    description="A Boolean value indicating whether or not a string attribute is case sensitive.",
                    required=False,
                    mutability=Mutability.READ_ONLY,
                    returned=Returned.DEFAULT,
                    uniqueness=Uniqueness.NONE,
                ),
                SchemaAttribute(
                    name="mutability",
                    type=AttributeType.STRING,
                    multi_valued=False,
                    description="Indicates whether or not an attribute is modifiable.",
                    required=False,
                    case_exact=True,
                    mutability=Mutability.READ_ONLY,
                    returned=Returned.DEFAULT,
                    uniqueness=Uniqueness.NONE,
                    canonical_values=[
                        "readOnly",
                        "readWrite",
                        "immutable",
                        "writeOnly",
                    ],
                ),
                SchemaAttribute(
                    name="returned",
                    type=AttributeType.STRING,
                    multi_valued=False,
                    description="Indicates whether or not an attribute is returned in a response (e.g., to a query).",
                    required=False,
                    case_exact=True,
                    mutability=Mutability.READ_ONLY,
                    returned=Returned.DEFAULT,
                    uniqueness=Uniqueness.NONE,
                    canonical_values=["always", "never", "default", "request"],
                ),
                SchemaAttribute(
                    name="uniqueness",
                    type=AttributeType.STRING,
                    multi_valued=False,
                    description="Indicates how unique a value must be.",
                    required=False,
                    case_exact=True,
                    mutability=Mutability.READ_ONLY,
                    returned=Returned.DEFAULT,
                    uniqueness=Uniqueness.NONE,
                    canonical_values=["none", "server", "global"],
                ),
                SchemaAttribute(
                    name="referenceTypes",
                    type=AttributeType.STRING,
                    multi_valued=True,
                    description="Used only with an attribute of type 'reference'. Specifies a SCIM resourceType that a reference attribute MAY refer to, e.g., 'User'.",
                    required=False,
                    case_exact=True,
                    mutability=Mutability.READ_ONLY,
                    returned=Returned.DEFAULT,
                    uniqueness=Uniqueness.NONE,
                ),
                SchemaAttribute(
                    name="subAttributes",
                    type=AttributeType.COMPLEX,
                    multi_valued=True,
                    description="Used to define the sub-attributes of a complex attribute.",
                    required=False,
                    mutability=Mutability.READ_ONLY,
                    returned=Returned.DEFAULT,
                    uniqueness=Uniqueness.NONE,
                    sub_attributes=[
                        SchemaAttribute(
                            name="name",
                            type=AttributeType.STRING,
                            multi_valued=False,
                            description="The attribute's name.",
                            required=True,
                            case_exact=True,
                            mutability=Mutability.READ_ONLY,
                            returned=Returned.DEFAULT,
                            uniqueness=Uniqueness.NONE,
                        ),
                        SchemaAttribute(
                            name="type",
                            type=AttributeType.STRING,
                            multi_valued=False,
                            description="The attribute's data type. Valid values include 'string', 'complex', 'boolean', 'decimal', 'integer', 'dateTime', 'reference'.",
                            required=True,
                            canonical_values=[
                                "string",
                                "complex",
                                "boolean",
                                "decimal",
                                "integer",
                                "dateTime",
                                "reference",
                            ],
                            case_exact=False,
                            mutability=Mutability.READ_ONLY,
                            returned=Returned.DEFAULT,
                            uniqueness=Uniqueness.NONE,
                        ),
                        SchemaAttribute(
                            name="multiValued",
                            type=AttributeType.BOOLEAN,
                            multi_valued=False,
                            description="A Boolean value indicating an attribute's plurality.",
                            required=True,
                            mutability=Mutability.READ_ONLY,
                            returned=Returned.DEFAULT,
                            uniqueness=Uniqueness.NONE,
                        ),
                        SchemaAttribute(
                            name="description",
                            type=AttributeType.STRING,
                            multi_valued=False,
                            description="A human-readable description of the attribute.",
                            required=False,
                            case_exact=True,
                            mutability=Mutability.READ_ONLY,
                            returned=Returned.DEFAULT,
                            uniqueness=Uniqueness.NONE,
                        ),
                        SchemaAttribute(
                            name="required",
                            type=AttributeType.BOOLEAN,
                            multi_valued=False,
                            description="A boolean value indicating whether or not the attribute is required.",
                            required=False,
                            mutability=Mutability.READ_ONLY,
                            returned=Returned.DEFAULT,
                            uniqueness=Uniqueness.NONE,
                        ),
                        SchemaAttribute(
                            name="canonicalValues",
                            type=AttributeType.STRING,
                            multi_valued=True,
                            description="A collection of canonical values. When applicable, service providers MUST specify the canonical types, e.g., 'work', 'home'.",
                            required=False,
                            case_exact=True,
                            mutability=Mutability.READ_ONLY,
                            returned=Returned.DEFAULT,
                            uniqueness=Uniqueness.NONE,
                        ),
                        SchemaAttribute(
                            name="caseExact",
                            type=AttributeType.BOOLEAN,
                            multi_valued=False,
                            description="A Boolean value indicating whether or not a string attribute is case sensitive.",
                            required=False,
                            mutability=Mutability.READ_ONLY,
                            returned=Returned.DEFAULT,
                            uniqueness=Uniqueness.NONE,
                        ),
                        SchemaAttribute(
                            name="mutability",
                            type=AttributeType.STRING,
                            multi_valued=False,
                            description="Indicates whether or not an attribute is modifiable.",
                            required=False,
                            case_exact=True,
                            mutability=Mutability.READ_ONLY,
                            returned=Returned.DEFAULT,
                            uniqueness=Uniqueness.NONE,
                            canonical_values=[
                                "readOnly",
                                "readWrite",
                                "immutable",
                                "writeOnly",
                            ],
                        ),
                        SchemaAttribute(
                            name="returned",
                            type=AttributeType.STRING,
                            multi_valued=False,
                            description="Indicates whether or not an attribute is returned in a response (e.g., to a query).",
                            required=False,
                            case_exact=True,
                            mutability=Mutability.READ_ONLY,
                            returned=Returned.DEFAULT,
                            uniqueness=Uniqueness.NONE,
                            canonical_values=["always", "never", "default", "request"],
                        ),
                        SchemaAttribute(
                            name="uniqueness",
                            type=AttributeType.STRING,
                            multi_valued=False,
                            description="Indicates how unique a value must be.",
                            required=False,
                            case_exact=True,
                            mutability=Mutability.READ_ONLY,
                            returned=Returned.DEFAULT,
                            uniqueness=Uniqueness.NONE,
                            canonical_values=["none", "server", "global"],
                        ),
                        SchemaAttribute(
                            name="referenceTypes",
                            type=AttributeType.STRING,
                            multi_valued=True,
                            description="Used only with an attribute of type 'reference'. Specifies a SCIM resourceType that a reference attribute MAY refer to, e.g., 'User'.",
                            required=False,
                            case_exact=True,
                            mutability=Mutability.READ_ONLY,
                            returned=Returned.DEFAULT,
                            uniqueness=Uniqueness.NONE,
                        ),
                    ],
                ),
            ],
        ),
    ]

    def __init__(self):
        self.id = "urn:ietf:params:scim:schemas:core:2.0:Schema"
        self.name = "Schema"
        self.description = "Specifies the schema that describes a SCIM schema"
        self.attributes = self._SCHEMA_ATTRIBUTES


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
        addresses: List[str] = None,
        groups: List[str] = None,
        entitlements: List[str] = None,
        roles: List[str] = None,
        x509_certificates: List[str] = None,
    ):
        self.id = "urn:ietf:params:scim:schemas:core:2.0:User"
        self.name = "User"
        self.description = "User Account"
        self.endpoint = "/Users"

        self.user_name = user_name
        self.formatted = formatted
        self.family_name = family_name
        self.given_name = given_name
        self.middle_name = middle_name
        self.honorific_prefix = honorific_prefix
        self.honorific_suffix = honorific_suffix
        self.display_name = display_name
        self.nick_name = nick_name
        self.profile_url = profile_url
        self.title = title
        self.userType = userType
        self.preferred_language = preferred_language
        self.locale = locale
        self.timezone = timezone
        self.active = active
        self.password = password
        self.emails = emails
        self.phone_numbers = phone_numbers
        self.ims = ims
        self.photos = photos
        self.addresses = addresses
        self.groups = groups
        self.entitlements = entitlements
        self.roles = roles
        self.x509_certificates = x509_certificates


class Manager:
    def __init__(self, *, value: str, ref: str, display_name: str):
        self.value = value
        self.ref = ref
        self.display_name = display_name


# class EnterpriseUser(Schema):
#     def __init__(
#         self,
#         *,
#         employee_number: str,
#         cost_center: str,
#         organization: str,
#         division: str,
#         department: str,
#         manager: Dict[str, str]


class Group(Schema):
    def __init__(
        self,
        *,
        display_name: str,
        members: List[str] = None,
    ):
        self.id = "urn:ietf:params:scim:schemas:core:2.0:Group"
        self.name = "Group"
        self.description = "Group"
        self.endpoint = "/Groups"

        self.display_name = display_name
        self.members = members
