from typing import List

from fastapi import APIRouter, Body, Depends
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from app.models.cleaning import CleaningCreate, CleaningUpdate, CleaningPublic

from app.api.dependencies.database import get_repository
from app.db.repositories.cleanings import CleaningsRepository
from app.models.cleaning import CleaningCreate, CleaningPublic

router = APIRouter()


@router.delete("/{id}/", response_model=int, name="cleanings:delete-cleaning-by-id")
async def delete_cleaning_by_id(
    id: int = Path(..., ge=1, title="The ID of the cleaning to delete"),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> int:
    delete_id = await cleanings_repo.delete_cleaning_by_id(id=id)
    if not delete_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="No cleaning found with that id"
        )

    return delete_id


# Path(..., ge=1 ==. With ge=1, we're telling FastAPI that the
# cleaning id must be an integer greater than or equal to 1.
# If it's not, FastAPI will return an HTTP_422_UNPROCESSABLE_ENTITY
# exception for us.
@router.put(
    "/{id}/", response_model=CleaningPublic, name="cleanings:update-cleaning-by-id"
)
async def update_cleaning_by_id(
    id: int = Path(..., ge=1, title="The ID of the cleaning to update"),
    cleaning_update: CleaningUpdate = Body(..., embed=True),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    updated_cleaning = await cleanings_repo.update_cleaning(
        id=id, cleaning_update=cleaning_update
    )
    if not updated_cleaning:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="No cleaning found with that id."
        )
    return updated_cleaning


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


@router.get(
    "/", response_model=List[CleaningPublic], name="cleanings:get-all-cleanings"
)
async def get_all_cleanings(
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> List[CleaningPublic]:
    return await cleanings_repo.get_all_cleanings()
