# Tutorial
https://www.jeffastor.com/blog/up-and-running-with-fastapi-and-docker#environment-and-setup


# To run testing
- docker ps
- docker exec -it [containerid] bash
- pytest -v


# Endpoint ==> Method	Description
## /cleaning/ ==> POST ==> Create a new cleaning
## /cleaning/{id}/ ==>	GET ==>	Get a cleaning by id
## /cleaning/ ==> GET ==> Get all available cleanings
## /cleaning/{id}/ ==>	PUT ==>	Update a cleaning by id
## /cleaning/{id}/ ==>  DELETE ==>	Delete a cleaning by id

# Creating Endpoint in TDD
## -- Test:         write some test to reveal what code to write or correct (cause they failed).
## -- Route:        write route which is called by the test, and test again.
## -- Repository:   write the repository which is called by the route, and test again.

# Database/Tables
#### https://www.jeffastor.com/blog/designing-a-robust-user-model-in-a-fastapi-app
#### Example
#### https://www.jeffastor.com/blog/setting-up-user-profiles-in-fastapi#creating-user-profiles
- row back migrations: alembic downgrade base (login into your docker container)
- prepare your sql tables (for .e.g db/migrations/versions/create_users_table)
- add newly created create_users_table to upgrade and drop it at downgrade
- run migrations: alembic upgrade head
- prepare your pydantic models (create backend/app/models.user.py) for e.g
- create your test and watch it fail, because of route
- create your route and repository