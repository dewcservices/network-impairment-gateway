from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.interfaces.ibearer_repository import IBearerRepository


class BearerRepository(IBearerRepository):
    def __init__(self, db: Session):
        self.db = db

    async def create(self, bearer: any) -> any:
        # db_recipe = _model.Recipe(title=recipe.title, description=recipe.description, ingredients=recipe.ingredients, method=recipe.method, favourite=recipe.favourite)
        # self.db.add(db_recipe)
        # self.db.commit()
        # self.db.refresh(db_recipe)
        return {}

    async def get_all(self) -> List[any]:
        bearers: any = {}
        return self.db.query(bearers).all()

    async def get(self, id: int) -> any:
        bearers: any = {}
        db_bearer = self.db.query(bearers.Recipe).filter(bearers.id == id).first()

        if db_bearer is None:
            raise HTTPException(
                status_code=404, detail="sorry this recipe does not exist"
            )
        return db_bearer

    async def update(self, bearer: any, id: int) -> any:
        db_bearer = await self.get(id)
        # update
        self.db.commit()
        self.db.refresh(db_bearer)
        return db_bearer

    async def delete(self, id: int):
        bearers: any = {}
        self.db.query(bearers).filter(bearers.id == id).delete()
        self.db.commit()
