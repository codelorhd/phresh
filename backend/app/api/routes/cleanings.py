from typing import List

from fastapi import APIRouter, Body, Depends
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.api.dependencies.database import get_repository
from app.db.repositories.cleanings import CleaningsRepository
from app.models.cleaning import CleaningCreate, CleaningPublic

router = APIRouter()


# On Body(..., embed=True) below
# If we want it to expect JSON with a key new_cleaning
# and inside of it the model contents, we use the special
# Body parameter embed in the parameter default.

# https://www.jeffastor.com/blog/hooking-fastapi-endpoints-up-to-a-postgres-database
# By simply specifying the CleaningCreate Python type declaration for new_cleaning, FastAPI will:

# Read the body of the request as JSON.
# Convert the corresponding types.
# Validate the data.
# Respond with an error if validation fails, or provide the route with the model instance needed.


@router.post(
    "/",
    response_model=CleaningPublic,
    name="cleanings:create-cleaning",
    status_code=HTTP_201_CREATED,
)
async def create_new_cleaning(
    new_cleaning: CleaningCreate = Body(..., embed=True),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    created_cleaning = await cleanings_repo.create_cleaning(new_cleaning=new_cleaning)
    return created_cleaning


@router.get(
    "/{id}/", response_model=CleaningPublic, name="cleanings:get-cleaning-by-id"
)
async def get_cleaning_by_id(
    id: int,
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    cleaning = await cleanings_repo.get_cleaning_by_id(id=id)

    if not cleaning:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="No cleaning found with that id."
        )
    return cleaning


@router.get("/")
async def get_all_cleanings() -> List[dict]:
    cleanings = [
        {
            "id": 1,
            "name": "My house",
            "cleaning_type": "full_clean",
            "price_per_hour": 29.99,
        },
        {
            "id": 2,
            "name": "Someone else's house",
            "cleaning_type": "spot_clean",
            "price_per_hour": 19.99,
        },
    ]

    return cleanings
