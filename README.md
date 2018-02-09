# risk types handling
# version 1.002

This is the risktypes backend as described in https://github.com/IntuitiveWebSolutions/ProductDevelopmentProject

It uses Python, Flask and SQLAlchemy.
The data layer is defined in models.py. For the needs of the actual implementation,
the model classes also include a serialize property for JSON encoding of the corresponding object.
Although not required, there are definitions of risk type instances, and risk field instances.
An ERD of the model is presented in entity_diagram.pdf

The repository itself contains the implementation of the backend.
The implementation is using Postgres as database.

The REST API endpoints are defined in rest.py.
These are simple GET endpoints, as described in the requirements.
A full implementation should implement POST, DELETE endpoints for handling
CRUD operations on risk types, and risk type fields.

The required frontend is implemented in Vue.js using the Vuetify widgets.
The application is hosted at http://risk.iris.gr.

A generic zappa settings json file is included, for turning the backend into an AWS Lambda.
As the current backend implementation uses PostgreSQL, the actual settings should be based on AWS PostgreSQL RDS.
Of course the server-less implementation of the backend as AWS lambda, is not expected
to have a large number of synchronous clients to be active. In the case of a real application
with a large number of concurrent requests (1000 or more),
special handling of a connection pool to the database would need to be considered.
