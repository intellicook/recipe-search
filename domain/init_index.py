import argparse
import os

from sqlalchemy import select
from sqlalchemy.orm import Session
from tqdm import tqdm

from configs.domain import configs
from domain import embeddings
from infra import models
from infra.db import engine

if __name__ == "__main__":
    # Set the arguments
    parser = argparse.ArgumentParser(
        description="Initialize the index file for the recipe search"
    )

    parser.add_argument(
        "--path",
        type=str,
        help="The path to save the index file",
        default="index.faiss",
    )
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        help="The number of recipes to index",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str.lower,
        help="The embedding model to use",
        choices=embeddings.mapping.keys(),
        default=configs.embedding_model,
    )

    # Parse the arguments
    args = parser.parse_args()

    # Choose the model
    model_cls = embeddings.mapping[args.model]

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

        if args.count:
            stmt = stmt.limit(args.count)

        recipes = session.execute(stmt).scalars().all()

    # Create the index
    model = model_cls()

    for recipe in tqdm(recipes, desc="Indexing recipes"):
        model.add(recipe)

    # Save the index to file
    model.save_to_file(args.path)

    # Initialize the index file model
    index_file = models.IndexFileModel(path=args.path)

    # Commit the index file model to the database
    with Session(engine) as session:
        session.add(index_file)
        session.commit()
