import logging
import os
import threading
from dataclasses import dataclass
from typing import Callable, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from tqdm import tqdm

from configs.domain import configs
from domain import embeddings
from domain.embeddings.base import BaseEmbedding
from infra import models
from infra.db import engine


@dataclass
class IndexThread:
    """Indexing thread"""

    count: Optional[int] = None
    model: str = ""
    path: str = ""
    exception: Optional[Exception] = None
    thread: Optional[threading.Thread] = None

    @property
    def is_in_progress(self) -> bool:
        """Check if the indexing is in progress.

        Returns:
            bool: True if the indexing is in progress, False otherwise.
        """
        return self.thread and self.thread.is_alive()

    @property
    def is_complete(self) -> bool:
        """Check if the indexing is complete.

        Returns:
            bool: True if the indexing is complete, False otherwise.
        """
        return self.thread and not self.is_in_progress

    @property
    def is_successful(self) -> bool:
        """Check if the indexing was successful.

        Returns:
            bool: True if the indexing was successful, False otherwise.
        """
        return self.is_complete and not self.exception


logger = logging.getLogger(__name__)
index_thread = IndexThread()


def init_index(
    count: Optional[int] = None,
    model: str = configs.embedding_model,
    path: str = configs.default_faiss_index_path,
    on_complete: Optional[Callable[[], None]] = None,
) -> bool:
    """Initialize the index file.

    Arguments:
        count (Optional[int], optional): The number of recipes to index.
            Defaults to None.
        model (str, optional): The embedding model to use. Defaults to
            configs.embedding_model.
        path (str, optional): The path to save the index file. Defaults to
            configs.default_faiss_index_path.
        on_complete (Optional[Callable[[], None]], optional): The callback
            function to call when the indexing is complete. Defaults to None.

    Returns:
        bool: True if the initialization was successful, False if indexing
            is already in progress.
    """
    global index_thread

    if index_thread.is_in_progress:
        logger.error("Indexing already in progress")
        return False

    # Create a new thread for indexing
    index_thread = IndexThread(
        count=count,
        model=model,
        path=path,
        exception=None,
        thread=threading.Thread(
            target=_init_index,
            kwargs=dict(
                count=count, model=model, path=path, on_complete=on_complete
            ),
        ),
    )

    index_thread.thread.start()

    return True


def _init_index(
    count: Optional[int] = None,
    model: str = configs.embedding_model,
    path: str = configs.default_faiss_index_path,
    on_complete: Optional[Callable[[], None]] = None,
):
    try:
        # Choose the model
        model_cls = embeddings.mapping[model]

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
        model: BaseEmbedding = model_cls()

        for recipe in tqdm(recipes, desc="Indexing recipes"):
            model.add(recipe)

        # Save the index to file
        model.save_to_file(path)

        # Initialize the index file model
        index_file = models.IndexFileModel(path=path)

        # Commit the index file model to the database
        with Session(engine) as session:
            session.add(index_file)
            session.commit()

        # Callback
        if on_complete is not None:
            on_complete()
    except Exception as e:
        logger.error(f"Indexing failed: {e}")
        index_thread.exception = e
