import json
import uuid
from collections.abc import Generator
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlmodel import Session

from src.ai_models.gemini.exceptions import AIGenerationError
from src.ai_models.gemini.provider import GeminiProvider
from src.flashcards.models import Card, Collection, PracticeSession
from src.flashcards.schemas import (
    AIFlashcard,
    AIFlashcardCollection,
    CardCreate,
    CardUpdate,
    CollectionCreate,
    CollectionUpdate,
)
from src.flashcards.services import (
    _generate_ai_flashcards,
    _get_collection_cards,
    _save_ai_collection,
    check_collection_access,
    create_card,
    create_collection,
    delete_card,
    delete_collection,
    generate_ai_collection,
    get_card,
    get_card_by_id,
    get_card_with_collection,
    get_cards,
    get_collection,
    get_collections,
    get_or_create_practice_session,
    get_practice_card,
    get_practice_cards,
    get_practice_session,
    get_practice_sessions,
    record_practice_card_result,
    update_card,
    update_collection,
)
from src.users.schemas import UserCreate
from src.users.services import create_user
from tests.utils.utils import random_email, random_lower_string


def mock_get_provider() -> Generator[GeminiProvider, None, None]:
    mock_provider = AsyncMock(spec=GeminiProvider)
    yield mock_provider


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
        card_in = CardCreate(front=f"front {i}", back=f"back {i}")
        create_card(session=db, card_in=card_in, collection_id=collection.id)
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


@pytest.fixture
def test_practice_session(
    db: Session, test_collection: Collection, test_multiple_cards: list[Card]
) -> PracticeSession:
    session = get_or_create_practice_session(
        session=db, collection_id=test_collection.id, user_id=test_collection.user_id
    )
    return session


@pytest.fixture
def test_multiple_practice_sessions(
    db: Session,
    test_multiple_collections: list[Collection],
) -> list[PracticeSession]:
    sessions = []
    for i in range(3):
        session = get_or_create_practice_session(
            session=db,
            collection_id=test_multiple_collections[i].id,
            user_id=test_multiple_collections[i].user_id,
        )
        sessions.append(session)

    return sessions


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


def test_get_card_by_id(db: Session, test_card: Card):
    db_card = get_card_by_id(session=db, card_id=test_card.id)

    assert db_card is not None
    assert db_card.id == test_card.id


def test_get_card_by_nonexistent_id(db: Session):
    non_existent_card_id = uuid.uuid4()
    db_card = get_card_by_id(session=db, card_id=non_existent_card_id)

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


def test_delete_card(db: Session, test_collection: Collection, test_card: Card):
    delete_card(session=db, card=test_card)

    card = get_card_with_collection(
        session=db, card_id=test_card.id, user_id=test_collection.user_id
    )
    assert card is None


def test_check_collection_access(db: Session, test_collection: Collection):
    can_access = check_collection_access(
        session=db, collection_id=test_collection.id, user_id=test_collection.user_id
    )

    assert can_access is True


def test_check_collection_access_with_nonexistent_collection(
    db: Session, test_user: dict[str, Any]
):
    non_existent_collection_id = uuid.uuid4()
    can_access = check_collection_access(
        session=db, collection_id=non_existent_collection_id, user_id=test_user["id"]
    )

    assert can_access is False


def test_check_collection_access_with_other_user(
    db: Session, test_collection: Collection, test_other_user: dict[str, Any]
):
    can_access = check_collection_access(
        session=db, collection_id=test_collection.id, user_id=test_other_user["id"]
    )

    assert can_access is False


def test_get_or_create_practice_sessions(
    db: Session,
    test_collection: Collection,
    test_multiple_cards: list[Card],
    test_user: dict[str, Any],
):
    session = get_or_create_practice_session(
        session=db, collection_id=test_collection.id, user_id=test_collection.user_id
    )

    assert session is not None
    assert session.collection_id == test_collection.id
    assert session.user_id == test_user["id"]
    assert session.is_completed is False
    assert session.total_cards == len(test_multiple_cards)
    assert session.cards_practiced == 0
    assert session.correct_answers == 0
    assert session.created_at is not None
    assert session.updated_at is not None


def test_get_practice_session(
    db: Session,
    test_practice_session: PracticeSession,
    test_collection: Collection,
    test_user: dict[str, Any],
):
    session = get_practice_session(
        session=db,
        session_id=test_practice_session.id,
        user_id=test_practice_session.user_id,
    )

    assert session is not None
    assert session.collection_id == test_collection.id
    assert session.user_id == test_user["id"]
    assert session.is_completed is False
    assert session.total_cards == len(test_collection.cards)
    assert session.cards_practiced == 0
    assert session.correct_answers == 0
    assert session.created_at is not None
    assert session.updated_at is not None


def test_get_practice_sessions(
    db: Session,
    test_multiple_practice_sessions: list[PracticeSession],
    test_user: dict[str, Any],
):
    limit = 2
    db_sessions, count = get_practice_sessions(
        session=db, user_id=test_user["id"], limit=limit
    )

    assert count == len(test_multiple_practice_sessions)
    assert limit == len(db_sessions)
    # Verify the order
    for i in range(len(db_sessions) - 1):
        assert db_sessions[i].updated_at >= db_sessions[i + 1].updated_at


def test_get_practice_sessions_with_skip(
    db: Session,
    test_multiple_practice_sessions: list[PracticeSession],
    test_user: dict[str, Any],
):
    skip = 2
    limit = 2
    db_sessions, count = get_practice_sessions(
        session=db, user_id=test_user["id"], skip=skip, limit=limit
    )

    assert count == len(test_multiple_practice_sessions)
    assert 1 == len(db_sessions)  # Due to the total sessions is 3


def test_get_collection_cards(
    db: Session, test_collection: Collection, test_multiple_cards: list[Card]
):
    cards = _get_collection_cards(session=db, collection_id=test_collection.id)

    assert len(cards) == len(test_multiple_cards)


def test_get_practice_card(db: Session, test_collection: Collection, test_card: Card):
    session = get_or_create_practice_session(
        session=db, collection_id=test_collection.id, user_id=test_collection.user_id
    )

    card = get_practice_card(
        session=db,
        practice_session_id=session.id,
        card_id=test_card.id,
    )

    assert card is not None
    assert card.card_id == test_card.id
    assert card.is_correct is None
    assert card.is_practiced is False


def test_get_nonexistent_practice_card(
    db: Session, test_practice_session: PracticeSession
):
    non_existent_card_id = uuid.uuid4()
    card = get_practice_card(
        session=db,
        practice_session_id=test_practice_session.id,
        card_id=non_existent_card_id,
    )

    assert card is None


def test_get_practice_cards(db: Session, test_practice_session: PracticeSession):
    limit = 3
    cards, count = get_practice_cards(
        session=db, practice_session_id=test_practice_session.id, limit=limit
    )

    assert limit == len(cards)
    assert count == len(test_practice_session.practice_cards)
    for card in cards:
        assert card.is_practiced is False
        assert card.is_correct is None


def test_get_practice_cards_with_status(
    db: Session, test_practice_session: PracticeSession
):
    cards, count = get_practice_cards(
        session=db, practice_session_id=test_practice_session.id
    )

    record_practice_card_result(session=db, practice_card=cards[0], is_correct=True)
    record_practice_card_result(session=db, practice_card=cards[1], is_correct=True)

    complete_count = 2
    cards, count = get_practice_cards(
        session=db, practice_session_id=test_practice_session.id, status="completed"
    )

    assert count == complete_count
    assert len(cards) == complete_count
    for card in cards:
        assert card.is_practiced is True
        assert card.is_correct is True

    cards, count = get_practice_cards(
        session=db, practice_session_id=test_practice_session.id, status="pending"
    )

    assert len(cards) == len(test_practice_session.practice_cards) - complete_count
    for card in cards:
        assert card.is_practiced is False
        assert card.is_correct is None


def test_get_practice_card_with_asc_order(
    db: Session, test_practice_session: PracticeSession
):
    cards, _ = get_practice_cards(
        session=db, practice_session_id=test_practice_session.id, order="asc"
    )

    # Verify the order
    for i in range(len(cards) - 1):
        assert cards[i].updated_at <= cards[i + 1].updated_at


def test_get_practice_card_with_desc_order(
    db: Session, test_practice_session: PracticeSession
):
    cards, _ = get_practice_cards(
        session=db, practice_session_id=test_practice_session.id, order="desc"
    )

    # Verify the order
    for i in range(len(cards) - 1):
        assert cards[i].updated_at >= cards[i + 1].updated_at


def test_record_practice_card_result(
    db: Session, test_practice_session: PracticeSession
):
    before_card = test_practice_session.practice_cards[0]
    original_updated_at = before_card.updated_at

    import time

    time.sleep(0.01)

    after_card = record_practice_card_result(
        session=db, practice_card=before_card, is_correct=True
    )

    session = get_practice_session(
        session=db,
        session_id=test_practice_session.id,
        user_id=test_practice_session.user_id,
    )

    assert session.correct_answers == 1
    assert session.cards_practiced == 1
    assert session.total_cards == len(test_practice_session.practice_cards)
    assert session.is_completed is False
    assert after_card.updated_at > original_updated_at
    assert after_card.is_correct is True
    assert after_card.is_practiced is True

    for card in test_practice_session.practice_cards[0:]:
        record_practice_card_result(session=db, practice_card=card, is_correct=True)

    session = get_practice_session(
        session=db,
        session_id=test_practice_session.id,
        user_id=test_practice_session.user_id,
    )

    # assert session.is_completed is True
    assert session.cards_practiced == len(test_practice_session.practice_cards)
    assert session.correct_answers == len(test_practice_session.practice_cards)


@pytest.mark.asyncio
async def test_generate_ai_collection():
    mock_session = MagicMock()
    mock_provider = AsyncMock()
    user_id = uuid.uuid4()

    test_cards = [AIFlashcard(front="Question 1", back="Answer 1")]
    ai_collection = AIFlashcardCollection(name="AI Generated", cards=test_cards)
    db_collection = Collection(name="AI Generated", user_id=user_id)

    with (
        patch(
            "src.flashcards.services._generate_ai_flashcards", new_callable=AsyncMock
        ) as mock_generate,
        patch("src.flashcards.services._save_ai_collection") as mock_save,
    ):
        mock_generate.return_value = ai_collection
        mock_save.return_value = db_collection

        result = await generate_ai_collection(
            session=mock_session,
            user_id=user_id,
            prompt="Create pytest flashcards",
            provider=mock_provider,
        )

        assert result == db_collection

        mock_generate.assert_called_once_with(mock_provider, "Create pytest flashcards")
        mock_save.assert_called_once_with(mock_session, user_id, ai_collection)


def test_save_ai_collection():
    mock_session = MagicMock()
    user_id = uuid.uuid4()

    def mock_refresh(obj):
        if isinstance(obj, Collection) and obj.id is None:
            obj.id = uuid.uuid4()

    mock_session.refresh.side_effect = mock_refresh

    test_cards = [
        AIFlashcard(front="Question 1", back="Answer 1"),
        AIFlashcard(front="Question 2", back="Answer 2"),
    ]

    test_collection = AIFlashcardCollection(name="Test Collection", cards=test_cards)

    result = _save_ai_collection(mock_session, user_id, test_collection)

    assert result.name == "Test Collection"
    assert result.user_id == user_id

    assert mock_session.add.call_count == 3  # 1 collection + 2 cards
    assert mock_session.commit.call_count == 2
    assert mock_session.refresh.call_count == 2  # Collection refreshed twice


@pytest.mark.asyncio
async def test_generate_ai_flashcards_success():
    mock_provider = AsyncMock()
    mock_get_config = MagicMock()

    # Setup run_model return value
    valid_json_response = json.dumps(
        {
            "collection": {
                "name": "AI Collection",
                "cards": [
                    {"front": "Question 1", "back": "Answer 1"},
                    {"front": "Question 2", "back": "Answer 2"},
                ],
            }
        }
    )
    mock_provider.run_model.return_value = valid_json_response

    with patch(
        "src.flashcards.services.get_flashcard_config", return_value=mock_get_config
    ):
        result = await _generate_ai_flashcards(
            mock_provider, "Create flashcards about Pytest"
        )

        assert result.name == "AI Collection"
        assert len(result.cards) == 2
        assert result.cards[0].front == "Question 1"
        assert result.cards[0].back == "Answer 1"

        mock_provider.run_model.assert_called_once_with(
            mock_get_config, "Create flashcards about Pytest"
        )


@pytest.mark.asyncio
async def test_generate_ai_flashcards_invalid_json():
    mock_provider = AsyncMock()
    mock_provider.run_model.return_value = "Invalid JSON"

    with patch("src.flashcards.services.get_flashcard_config"):
        with pytest.raises(
            AIGenerationError, match="Failed to parse AI response as JSON"
        ):
            await _generate_ai_flashcards(mock_provider, "Create flashcards")


@pytest.mark.asyncio
async def test_generate_ai_flashcards_missing_collection():
    mock_provider = AsyncMock()
    mock_provider.run_model.return_value = json.dumps({"other_field": "value"})

    with patch("src.flashcards.services.get_flashcard_config"):
        with pytest.raises(
            AIGenerationError, match="AI response missing 'collection' field"
        ):
            await _generate_ai_flashcards(mock_provider, "Create flashcards")


@pytest.mark.asyncio
async def test_generate_ai_flashcards_empty_cards():
    mock_provider = AsyncMock()
    mock_provider.run_model.return_value = json.dumps(
        {"collection": {"name": "Empty Collection", "cards": []}}
    )

    with patch("src.flashcards.services.get_flashcard_config"):
        with pytest.raises(
            AIGenerationError, match="AI generated an empty collection with no cards"
        ):
            await _generate_ai_flashcards(mock_provider, "Create flashcards")
