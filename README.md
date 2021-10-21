# scimterface

A SCIM 2.0 interface that allows you to map SCIM endpoints to underlying system logic. Useful for creating SCIM wrappers around non-SCIM APIs.

## To Use
1. Create a new .py file in the `systems` directory. The name of the file (minus the .py) will be the systemCreate a subclass of the System class and write custom fetch logic for each endpoint.

### Style
Code should be formatted using [black](https://github.com/psf/black).