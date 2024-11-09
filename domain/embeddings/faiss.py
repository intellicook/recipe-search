import logging
import os
import threading
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Literal, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from tqdm import tqdm

from configs.domain import configs
from domain import embeddings
from domain.embeddings.base import BaseEmbedding
from infra import models
from infra.db import engine
from protos.faiss_index_thread_pb2 import (
    FaissIndexThreadArgs,
    FaissIndexThreadResponse,
    FaissIndexThreadStatus,
)


@dataclass
class IndexThread:
    """Indexing thread"""

    class Status(Enum):
        """Indexing status"""

        UNINITIALIZED = auto()
        IN_PROGRESS = auto()
        FAILED = auto()
        COMPLETED = auto()

        def to_proto(self) -> FaissIndexThreadStatus:
            """Convert the status to a protobuf message.

            Returns:
                FaissIndexThreadStatus: The protobuf message.
            """
            return FaissIndexThreadStatus.Value(self.name)

    count: int = 0
    model: str = ""
    path: str = ""
    exception: Optional[Exception] = None
    thread: Optional[threading.Thread | Literal["Database"]] = None

    @property
    def status(self) -> Status:
        """Get the indexing status.

        Returns:
            IndexThread.Status: The indexing status.
        """
        if not self.thread:
            return IndexThread.Status.UNINITIALIZED
        elif (
            isinstance(self.thread, threading.Thread)
            and self.thread.is_alive()
        ):
            return IndexThread.Status.IN_PROGRESS
        elif self.exception:
            return IndexThread.Status.FAILED
        else:
            return IndexThread.Status.COMPLETED

    def to_proto(self) -> FaissIndexThreadResponse:
        """Convert the indexing thread to a protobuf message.

        Returns:
            FaissIndexThreadResponse: The protobuf message.
        """
        args = None
        if self.status != IndexThread.Status.UNINITIALIZED:
            args = FaissIndexThreadArgs(
                count=self.count,
                model=self.model,
                path=self.path,
            )

        return FaissIndexThreadResponse(
            status=self.status.to_proto(), args=args
        )


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

    if index_thread.status == IndexThread.Status.IN_PROGRESS:
        logger.error("Indexing already in progress")
        return False

    # Get number of recipes in database if count is None
    if count is None:
        with Session(engine) as session:
            stmt = select(func.count()).select_from(models.RecipeModel)
            count = session.execute(stmt).scalar()

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
    count: int,
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
            stmt = select(models.RecipeModel).limit(count)
            recipes = session.execute(stmt).scalars().all()

        # Create the index
        embedding: BaseEmbedding = model_cls()

        for recipe in tqdm(recipes, desc="Indexing recipes"):
            embedding.add(recipe)

        # Save the index to file
        embedding.save_to_file(path)

        # Initialize the index file model
        index_file = models.IndexFileModel(
            count=count,
            model=model,
            path=path,
        )

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
