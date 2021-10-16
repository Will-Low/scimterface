class System:
    def _create_error_text(self, method: str, endpoint: str) -> str:
        return f"The {method} method is not implemented for {endpoint}"

    def get_users(self):
        raise NotImplementedError(self._create_error_text("GET", "/Users"))

    def post_users(self):
        raise NotImplementedError(self._create_error_text("POST", "/Users"))

    def put_users(self):
        raise NotImplementedError(self._create_error_text("PUT", "/Users"))

    def patch_users(self):
        raise NotImplementedError(self._create_error_text("PATCH", "/Users"))

    def delete_users(self):
        raise NotImplementedError(self._create_error_text("DELETE", "/Users"))

    def get_groups(self):
        raise NotImplementedError(self._create_error_text("GET", "/Groups"))

    def post_groups(self):
        raise NotImplementedError(self._create_error_text("POST", "/Groups"))

    def put_groups(self):
        raise NotImplementedError(self._create_error_text("PUT", "/Groups"))

    def patch_groups(self):
        raise NotImplementedError(self._create_error_text("PATCH", "/Groups"))

    def delete_groups(self):
        raise NotImplementedError(self._create_error_text("DELETE", "/Groups"))

    def get_me(self):
        raise NotImplementedError(self._create_error_text("GET", "/Me"))

    def post_me(self):
        raise NotImplementedError(self._create_error_text("POST", "/Me"))

    def put_me(self):
        raise NotImplementedError(self._create_error_text("PUT", "/Me"))

    def patch_me(self):
        raise NotImplementedError(self._create_error_text("PATCH", "/Me"))

    def delete_me(self):
        raise NotImplementedError(self._create_error_text("DELETE", "/Me"))

    def get_service_provider_config(self):
        raise NotImplementedError(self._create_error_text("GET", "/ServiceProviderConfig"))

    def get_resource_types(self):
        raise NotImplementedError(self._create_error_text("GET", "/ResourceTypes"))

    def get_schemas(self):
        raise NotImplementedError(self._create_error_text("GET", "/Schemas"))

    def post_bulk(self):
        raise NotImplementedError(self._create_error_text("POST", "/Bulk"))

    def post_search(self):
        raise NotImplementedError(self._create_error_text("POST", "/.search"))
