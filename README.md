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
## - Write the test and let them fail
## - Write whatever code needed to get the test run

### - Write the test
### - Run the test
### - Correct Error: write the endpoint and allow it fail (pytest is gracious enough to tell us exactly what's happening)
### - Correct/Fix up
### - Retry till all tests are completed