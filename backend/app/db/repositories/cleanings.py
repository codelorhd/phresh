from typing import List

from fastapi.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from app.db.repositories.base import BaseRepository
from app.models.cleaning import (
    CleaningCreate,
    CleaningPublic,
    CleaningUpdate,
    CleaningInDB,
)


CREATE_CLEANING_QUERY = """
    INSERT INTO cleanings (name, description, price, cleaning_type)
    VALUES (:name, :description, :price, :cleaning_type)
    RETURNING id, name, description, price, cleaning_type;
"""

GET_CLEANING_BY_ID_QUERY = """
    SELECT id, name, description, price, cleaning_type
    FROM cleanings
    WHERE id = :id;
"""

GET_ALL_CLEANINGS_QUERY = """
    SELECT id, name, description, price, cleaning_type  
    FROM cleanings;  
"""

# https://www.postgresql.org/docs/current/sql-update.html
# The optional RETURNING clause causes UPDATE to compute and
# return value(s) based on each row actually updated. Any
# expression using the table's columns, and/or columns of
# other tables mentioned in FROM, can be computed. The new
# (post-update) values of the table's columns are used. The
# syntax of the RETURNING list is identical to that of the
# output list of SELECT.
UPDATE_CLEANING_BY_ID_QUERY = """
    UPDATE cleanings  
    SET name         = :name,  
        description  = :description,  
        price        = :price,  
        cleaning_type = :cleaning_type  
    WHERE id = :id  
    RETURNING id, name, description, price, cleaning_type;  
"""

DELETE_CLEANING_BY_ID_QUERY = """
DELETE FROM cleanings
WHERE id = :id
RETURNING id;
"""


class CleaningsRepository(BaseRepository):
    """ "
    All database actions associated with the Cleaning resource
    """

    async def get_all_cleanings(self) -> List[CleaningPublic]:
        cleaning_records = await self.db.fetch_all(query=GET_ALL_CLEANINGS_QUERY)
        return [CleaningInDB(**l) for l in cleaning_records]

    async def create_cleaning(self, *, new_cleaning: CleaningCreate) -> CleaningInDB:
        query_values = new_cleaning.dict()
        cleaning = await self.db.fetch_one(
            query=CREATE_CLEANING_QUERY, values=query_values
        )

        return CleaningInDB(**cleaning)

    async def get_cleaning_by_id(self, *, id: int) -> CleaningInDB:
        cleaning = await self.db.fetch_one(GET_CLEANING_BY_ID_QUERY, values={"id": id})

        if not cleaning:
            return None

        return CleaningInDB(**cleaning)

    async def update_cleaning(
        self, *, id: int, cleaning_update: CleaningUpdate
    ) -> CleaningInDB:
        cleaning = await self.get_cleaning_by_id(id=id)

        if not cleaning:
            return None

        """
        As specified in pydantic docs, we can call the .copy() method 
        on the model and pass any changes we'd like to make to the 
        update parameter. Pydantic indicates that update should be 
        "a dictionary of values to change when creating the copied model", 
        and we obtain that by calling the .dict() method on the CleaningUpdate 
        model we received in our PUT route. By specifying exclude_unset=True, 
        Pydantic will leave out any attributes that were not explicitly 
        set when the model was created.
        """
        cleaning_update_params = cleaning.copy(
            update=cleaning_update.dict(exclude_unset=True)
        )

        # Note that because we listed "cleaning_type" with an
        # Optional type specification in our CleaningUpdate
        # Any time a user pass None as the cleaning_type,
        # throw an error.
        if cleaning_update_params.cleaning_type is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid cleaning type. Cannot be None.",
            )
        try:
            updated_cleaning = await self.db.fetch_one(
                query=UPDATE_CLEANING_BY_ID_QUERY, values=cleaning_update_params.dict()
            )
            return CleaningInDB(**updated_cleaning)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Invalid update params."
            )

    async def delete_cleaning_by_id(self, *, id: int) -> int:
        cleaning = await self.get_cleaning_by_id(id=id)
        if not cleaning:
            return None

        deleted_id = await self.db.execute(query=DELETE_CLEANING_BY_ID_QUERY)
        return deleted_id