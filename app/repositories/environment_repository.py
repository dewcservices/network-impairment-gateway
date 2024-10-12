from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.interfaces.ienvironment_repository import IEnvironmentRepository


class EnvironmentRepository(IEnvironmentRepository):
    def __init__(self, db: Session):
        self.db = db

    async def create(self, env: any) -> any:
        # db_recipe = _model.Recipe(title=recipe.title, description=recipe.description, ingredients=recipe.ingredients, method=recipe.method, favourite=recipe.favourite)
        # self.db.add(db_recipe)
        # self.db.commit()
        # self.db.refresh(db_recipe)
        return {}

    async def get_all(self) -> List[any]:
        env: any = {}
        return self.db.query(env).all()

    async def get(self, id: int) -> any:
        env: any = {}
        db_env = self.db.query(env.Recipe).filter(env.id == id).first()

        if db_env is None:
            raise HTTPException(
                status_code=404, detail="sorry this recipe does not exist"
            )
        return db_env

    async def update(self, env: any, id: int) -> any:
        db_env = await self.get(id)
        # update
        self.db.commit()
        self.db.refresh(db_env)
        return db_env

    async def delete(self, id: int):
        env: any = {}
        self.db.query(env).filter(env.id == id).delete()
        self.db.commit()
