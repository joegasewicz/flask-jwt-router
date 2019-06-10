Configuration
=============


Configuration options available:

Options for Flask's `app.config` object.

==================   ===================   ========================
Option Name           Type                  Description
==================   ===================   ========================
WHITE_LIST_ROUTES    `List` of `Tuples`     List of tuple pairs of `verb` & `path` strings
ENTITY_KEY           `string`               Optional. The entity model primary key name. Default is set to `id`
SECRET_KEY           `string`               Required (although optional). This key is used to create the token & must be kept secret.
==================   ===================   ========================

Options for `JwtRoutes` class

==================   ===================   ========================
Option Name           Type                  Description
==================   ===================   ========================
app                   Flask App instance    Required
entity_model          SQLAlchemy Model      Optional
exp                   int                   Optional (default is 30) Defines the amount of days before the token expires.
==================   ===================   ========================

Options for `RouteHelpers` class

==================   ===================   ========================
Option Name           Type                  Description
==================   ===================   ========================
app                   Flask App instance    Required.
==================   ===================   ========================

Options for `RouteHelpers.register_entity` methods

==================   ===================   ========================
Option Name           Type                  Description
==================   ===================   ========================
entity_id            `string`               Required. Entity model primary key.
==================   ===================   ========================

Options for `RouteHelpers.update_entity` methods

==================   ===================   ========================
Option Name           Type                  Description
==================   ===================   ========================
entity_id            `string`               Required. Entity model primary key.
==================   ===================   ========================