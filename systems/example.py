import json

from scim_system import SCIMSystem
import scim_utilities


class Example(SCIMSystem):
    users = [scim_utilities.User(user_name="bob")]

    def get_users(self):
        return json.dumps(self.users)
