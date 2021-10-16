from scim import NotImplemented

class System:
    def get_users(self):
        raise NotImplemented("GET", "/Users")

    def post_users(self):
        raise NotImplemented("POST", "/Users")

    def put_users(self):
        raise NotImplemented("PUT", "/Users")

    def patch_users(self):
        raise NotImplemented("PATCH", "/Users")

    def delete_users(self):
        raise NotImplemented("DELETE", "/Users")

    def get_groups(self):
        raise NotImplemented("GET", "/Groups")

    def post_groups(self):
        raise NotImplemented("POST", "/Groups")

    def put_groups(self):
        raise NotImplemented("PUT", "/Groups")

    def patch_groups(self):
        raise NotImplemented("PATCH", "/Groups")

    def delete_groups(self):
        raise NotImplemented("DELETE", "/Groups")

    def get_me(self):
        raise NotImplemented("GET", "/Me")

    def post_me(self):
        raise NotImplemented("POST", "/Me")

    def put_me(self):
        raise NotImplemented("PUT", "/Me")

    def patch_me(self):
        raise NotImplemented("PATCH", "/Me")

    def delete_me(self):
        raise NotImplemented("DELETE", "/Me")

    def get_service_provider_config(self):
        raise NotImplemented("GET", "/ServiceProviderConfig")

    def get_resource_types(self):
        raise NotImplemented("GET", "/ResourceTypes")

    def get_schemas(self):
        raise NotImplemented("GET", "/Schemas")

    def post_bulk(self):
        raise NotImplemented("POST", "/Bulk")

    def post_search(self):
        raise NotImplemented("POST", "/.search")
