import uuid
from typing import Any

import pytest
from sqlmodel import Session

from src.flashcards.models import Card, Collection
from src.flashcards.schemas import (
    CardCreate,
    CardUpdate,
    CollectionCreate,
    CollectionUpdate,
)
from src.flashcards.services import (
    create_card,
    create_collection,
    delete_collection,
    get_card,
    get_card_with_collection,
    get_cards,
    get_collection,
    get_collections,
    update_card,
    update_collection,
)
from src.users.schemas import UserCreate
from src.users.services import create_user
from tests.utils.utils import random_email, random_lower_string


@pytest.fixture
def test_user(db: Session) -> dict[str, Any]:
    email = random_email()
    password = random_lower_string()
    full_name = random_lower_string()

    user_in = UserCreate(email=email, password=password, full_name=full_name)
    user = create_user(session=db, user_create=user_in)

    return {"id": user.id, "email": user.email}


@pytest.fixture
def test_other_user(db: Session) -> dict[str, Any]:
    email = random_email()
    password = random_lower_string()
    full_name = random_lower_string()

    user_in = UserCreate(email=email, password=password, full_name=full_name)
    user = create_user(session=db, user_create=user_in)

    return {"id": user.id, "email": user.email}


@pytest.fixture
def test_collection(db: Session, test_user: dict[str, Any]) -> Collection:
    collection_in = CollectionCreate(name="Test Collection")
    collection = create_collection(
        session=db,
        collection_in=collection_in,
        user_id=test_user["id"],
    )

    return collection


@pytest.fixture
def test_multiple_collections(
    db: Session, test_user: dict[str, Any]
) -> list[Collection]:
    collections = []

    for i in range(5):
        collection_in = CollectionCreate(name=f"Test Collection {i}")
        collection = create_collection(
            session=db,
            collection_in=collection_in,
            user_id=test_user["id"],
        )
        collections.append(collection)

    return collections


@pytest.fixture
def test_card(db: Session, test_collection: Collection) -> Card:
    card_in = CardCreate(front="front", back="back")
    card = create_card(session=db, card_in=card_in, collection_id=test_collection.id)
    return card


@pytest.fixture
def test_multiple_cards(db: Session, test_collection: Collection) -> list[Card]:
    cards = []
    for i in range(5):
        card_in = CardCreate(front=f"front {i}", back=f"back {i}")
        card = create_card(
            session=db, card_in=card_in, collection_id=test_collection.id
        )
        cards.append(card)

    return cards


def test_create_collection(db: Session, test_user: dict[str, Any]):
    collection_in = CollectionCreate(name="Test Collection")
    collection = create_collection(
        session=db,
        collection_in=collection_in,
        user_id=test_user["id"],
    )

    assert collection.id is not None
    assert collection.name == collection_in.name
    assert collection.user_id == test_user["id"]
    assert collection.created_at is not None
    assert collection.updated_at is not None


def test_get_collection(
    db: Session, test_user: dict[str, Any], test_collection: Collection
):
    db_collection = get_collection(
        session=db, id=test_collection.id, user_id=test_user["id"]
    )
    assert db_collection is not None
    assert db_collection.id == test_collection.id
    assert db_collection.name == test_collection.name
    assert db_collection.user_id == test_user["id"]


def test_get_collection_not_found(db: Session, test_user: dict[str, Any]):
    db_collection = get_collection(session=db, id=uuid.uuid4(), user_id=test_user["id"])
    assert db_collection is None


def test_get_collection_with_wrong_user(db: Session, test_other_user: dict[str, Any]):
    db_collection = get_collection(
        session=db, id=uuid.uuid4(), user_id=test_other_user["id"]
    )
    assert db_collection is None


def test_get_collections(
    db: Session, test_user: dict[str, Any], test_multiple_collections: list[Collection]
):
    limit = 2
    db_collections, count = get_collections(
        session=db, user_id=test_user["id"], limit=limit
    )

    assert len(db_collections) == limit
    assert count == len(test_multiple_collections)

    # Verify the order
    for i in range(len(db_collections) - 1):
        assert db_collections[i].updated_at >= db_collections[i + 1].updated_at


def test_get_collection_skip(
    db: Session, test_user: dict[str, Any], test_multiple_collections: list[Collection]
):
    skip = 2
    limit = 2

    db_collections, count = get_collections(
        session=db, user_id=test_user["id"], skip=skip, limit=limit
    )

    assert len(db_collections) == limit
    assert count == len(test_multiple_collections)


def test_get_collection_empty(db: Session, test_user: dict[str, Any]):
    db_collections, count = get_collections(session=db, user_id=test_user["id"])

    assert len(db_collections) == 0
    assert count == 0


def test_update_collection(db: Session, test_collection: Collection):
    original_updated_at = test_collection.updated_at

    import time

    time.sleep(0.01)

    collection_in = CollectionUpdate(name="Updated Collection")
    collection_update = update_collection(
        session=db, collection=test_collection, collection_in=collection_in
    )

    assert collection_update is not None
    assert collection_update.name == collection_in.name
    assert collection_update.updated_at > original_updated_at


def test_delete_collection(
    db: Session, test_user: dict[str, Any], test_collection: Collection
):
    delete_collection(session=db, collection=test_collection)

    db_collection = get_collection(
        session=db, id=test_collection.id, user_id=test_user["id"]
    )

    assert db_collection is None


def test_create_card(db: Session, test_collection: Collection):
    card_in = CardCreate(front="front", back="back")
    card = create_card(session=db, card_in=card_in, collection_id=test_collection.id)

    assert card is not None
    assert card.id is not None
    assert card.front == card_in.front
    assert card.back == card_in.back
    assert card.collection_id == test_collection.id
    assert card.created_at is not None
    assert card.updated_at is not None


def test_get_card(db: Session, test_card: Card):
    db_card = get_card(session=db, card_id=test_card.id)

    assert db_card is not None
    assert db_card.id == test_card.id
    assert db_card.front == test_card.front
    assert db_card.back == test_card.back
    assert db_card.collection_id == test_card.collection_id
    assert db_card.updated_at is not None
    assert db_card.created_at is not None


def test_get_card_not_found(db: Session):
    db_card = get_card(session=db, card_id=uuid.uuid4())

    assert db_card is None


def test_get_card_with_collection(
    db: Session, test_collection: Collection, test_card: Card
):
    db_card = get_card_with_collection(
        session=db, card_id=test_card.id, user_id=test_collection.user_id
    )

    assert db_card is not None


def test_get_card_with_wrong_collection(db: Session, test_card: Card):
    db_card = get_card_with_collection(
        session=db,
        card_id=test_card.id,
        user_id=uuid.uuid4(),
    )

    assert db_card is None


def test_get_cards(
    db: Session, test_collection: Collection, test_multiple_cards: list[Card]
):
    limit = 3
    db_cards, count = get_cards(
        session=db, collection_id=test_collection.id, limit=limit
    )

    assert len(db_cards) == limit
    assert count == len(test_multiple_cards)
    # Verify the order
    for i in range(len(db_cards) - 1):
        assert db_cards[i].updated_at >= db_cards[i + 1].updated_at


def test_get_cards_skip(
    db: Session, test_collection: Collection, test_multiple_cards: list[Card]
):
    limit = 3
    skip = 2
    db_cards, count = get_cards(
        session=db, collection_id=test_collection.id, skip=skip, limit=limit
    )

    assert len(db_cards) == limit
    assert count == len(test_multiple_cards)


def test_get_cards_empty(db: Session, test_collection: Collection):
    db_cards, count = get_cards(session=db, collection_id=test_collection.id)

    assert len(db_cards) == 0
    assert count == 0


def test_update_card(db: Session, test_card: Card):
    original_updated_at = test_card.updated_at

    import time

    time.sleep(0.01)

    card_in = CardUpdate(front="Update front", back="Update back")
    updated_card = update_card(session=db, card=test_card, card_in=card_in)

    assert updated_card.front == card_in.front
    assert updated_card.back == card_in.back
    assert updated_card.updated_at > original_updated_at


def test_update_card_partial(db: Session, test_card: Card):
    original_updated_at = test_card.updated_at

    import time

    time.sleep(0.01)

    card_in = CardUpdate(front="Update front")
    updated_card = update_card(session=db, card=test_card, card_in=card_in)

    assert updated_card.front == card_in.front
    assert updated_card.back == test_card.back
    assert updated_card.updated_at > original_updated_at
