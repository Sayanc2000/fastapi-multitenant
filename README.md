# FastAPI (Multi-Tenant)

This is a multi-tenant backend for FastAPI.

### How to run with Docker

1. Clone the repository
2. Run `docker-compose up --build`
3. The backend will be running on `http://0.0.0.0:8000`
4. Detailed docs at `/redoc`

### How to run without Docker

1. Clone the repository
2. Run `rye sync`
3. Enter rye shell
4. Run `uvicorn main:app --reload`
5. The backend will be running on `http://0.0.0.0:8000`
6. Detailed docs at `/redoc`

## Project Structure

**Please note: Naming conventions are very strict and should to followed throughout the project. Moving away from them
may
cause unexpected results or errors**

### Models

* The project is setup to accommodate future tenants who can share a high amount of code.
* Tenants in the project are referred to as `Domain`.
* They are defined [here](./schemas/__init__.py)
* Base models are defined in [base_models.py](base_models.py)
* To extend on the base models, you can extend them under a new domain folder as in [here](tenant_a/models.py)

### Routers

* Routers a divided based on the resource in the DB.

### Controllers

* Router actions are encapsulated in [controllers](controllers)
* Each of the resource controller necessarily has a `base_<resource>.py` having a class `Base<Resource>`. This is the
  fallback option which will be initialized in case of no domain specific controller.
* Domain specific controllers should be defined in a file named `<domain>_<resource>.py` having a
  class `<Domain><Resource>`.
  For example, `tenanta_user.py` having a class `TenantaUser`

### Schemas

* Base schemas are defined in [schemas](schemas). Based on resource
* Every Schema follows the naming convention `Base<SchemaName>`
* Domain specific schemas should be defined in respective domain folder schemas for example [tenent_a](tenant_a/schemas)
* Domain specific schemas should be named `<Domain><SchemaName>`

### Headers

* `domain`: Needs to be provided by the client to gain access to the server and that is enforced using middleware