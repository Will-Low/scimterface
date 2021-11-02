import unittest

import scim_utilities


class TestSCIMUtilities(unittest.TestCase):
    def test_user_json_encode(self):
        user = scim_utilities.User(id="test@test.com", user_name="test@test.com")
        user_json = user.json_encode()

        expected = {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": "test@test.com",
            "userName": "test@test.com",
        }
        self.assertDictEqual(user_json, expected)


if __name__ == "__main__":
    unittest.main()
