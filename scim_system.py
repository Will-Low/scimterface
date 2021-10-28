"""Holds the base class for the SCIM system"""

from abc import ABC, abstractmethod


def _create_error_text(method: str, endpoint: str) -> str:
    return f"The {method} method is not implemented for {endpoint}"


class SCIMSystem(ABC):
    """Represents a system behind the SCIM 2.0 interface.
    Methods are named according to to RFC7644 section 3.2 and follow the pattern:
    <HTTP method>_<SCIM endpoint>
    """

    @abstractmethod
    def get_users(self):
        """GET /Users"""
        raise NotImplementedError(_create_error_text("GET", "/Users"))

    @abstractmethod
    def post_users(self):
        """POST /Users"""
        raise NotImplementedError(_create_error_text("POST", "/Users"))

    @abstractmethod
    def put_users(self):
        """PUT /Users"""
        raise NotImplementedError(_create_error_text("PUT", "/Users"))

    @abstractmethod
    def patch_users(self):
        """PATCH /Users"""
        raise NotImplementedError(_create_error_text("PATCH", "/Users"))

    @abstractmethod
    def delete_users(self):
        """DELETE /Users"""
        raise NotImplementedError(_create_error_text("DELETE", "/Users"))

    @abstractmethod
    def get_groups(self):
        """GET /Groups"""
        raise NotImplementedError(_create_error_text("GET", "/Groups"))

    @abstractmethod
    def post_groups(self):
        """POST /Groups"""
        raise NotImplementedError(_create_error_text("POST", "/Groups"))

    @abstractmethod
    def put_groups(self):
        """PUT /Groups"""
        raise NotImplementedError(_create_error_text("PUT", "/Groups"))

    @abstractmethod
    def patch_groups(self):
        """PATCH /Groups"""
        raise NotImplementedError(_create_error_text("PATCH", "/Groups"))

    @abstractmethod
    def delete_groups(self):
        """DELETE /Groups"""
        raise NotImplementedError(_create_error_text("DELETE", "/Groups"))

    @abstractmethod
    def get_me(self):
        """GET /Me"""
        raise NotImplementedError(_create_error_text("GET", "/Me"))

    @abstractmethod
    def post_me(self):
        """POST /Me"""
        raise NotImplementedError(_create_error_text("POST", "/Me"))

    @abstractmethod
    def put_me(self):
        """PUT /Me"""
        raise NotImplementedError(_create_error_text("PUT", "/Me"))

    @abstractmethod
    def patch_me(self):
        """PATCH /Me"""
        raise NotImplementedError(_create_error_text("PATCH", "/Me"))

    @abstractmethod
    def delete_me(self):
        """DELETE /Me"""
        raise NotImplementedError("DELETE", "/Me")

    @abstractmethod
    def get_service_provider_config(self):
        """GET /ServiceProviderConfig"""
        raise NotImplementedError("GET", "/ServiceProviderConfig")

    @abstractmethod
    def get_resource_types(self):
        """GET /ResourceTypes"""
        raise NotImplementedError("GET", "/ResourceTypes")

    @abstractmethod
    def get_schemas(self):
        """GET /Schemas"""
        raise NotImplementedError("GET", "/Schemas")

    @abstractmethod
    def post_bulk(self):
        """POST /Bulk"""
        raise NotImplementedError("POST", "/Bulk")

    @abstractmethod
    def post_search(self):
        """POST /.search"""
        raise NotImplementedError("POST", "/.search")
