import os
import sys

from sqlalchemy import select
from sqlalchemy.orm import Session
from tqdm import tqdm

from domain.stella import Stella
from infra import models
from infra.db import engine

if __name__ == "__main__":
    # Get argument
    if len(sys.argv) not in (2, 3):
        print(
            f"Usage: {sys.argv[0]} <path> [<count>]\n"
            "  <path> is the path to the index file\n"
            "  <count> is the number of recipes to index"
        )
        sys.exit(1)

    path = sys.argv[1]

    count = None
    if len(sys.argv) == 3:
        count = int(sys.argv[2])

    with Session(engine) as session:
        # Delete all index files
        stmt = select(models.IndexFileModel)
        index_files = session.execute(stmt).scalars().all()

        for index_file in index_files:
            if os.path.exists(index_file.path):
                os.remove(index_file.path)
            session.delete(index_file)

        session.commit()

        # Get the recipes
        stmt = select(models.RecipeModel)

        if count:
            stmt = stmt.limit(count)

        recipes = session.execute(stmt).scalars().all()

    # Create the index
    stella = Stella()

    for recipe in tqdm(recipes):
        stella.add_recipe(recipe)

    # Save the index to file
    stella.save_to_file(path)

    # Initialize the index file model
    index_file = models.IndexFileModel(path=path)

    with Session(engine) as session:
        session.add(index_file)
        session.commit()
