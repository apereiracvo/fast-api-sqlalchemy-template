from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.db.utils import transaction
from app.decks_schema import decks_schema
from app.models import decks_model


router = APIRouter()


@router.get("/decks/", response_model=decks_schema.Decks)
async def list_decks() -> Any:
    objects = await models.Deck.all()
    return {"items": objects}


@router.get("/decks/{deck_id}/", response_model=decks_schema.Deck)
async def get_deck(deck_id: UUID) -> Any:
    instance = await models.Deck.get_by_id(deck_id, prefetch=("cards",))
    if not instance:
        raise HTTPException(status_code=404, detail="Deck is not found")
    return instance


@router.put("/decks/{deck_id}/", response_model=decks_schema.Deck)
async def update_deck(deck_id: UUID, data: decks_schema.DeckCreate) -> Any:
    instance = await models.Deck.get_by_id(deck_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Deck is not found")
    await instance.update_attrs(**data.dict())
    await instance.save()
    return instance


@router.post("/decks/", response_model=decks_schema.Deck)
async def create_deck(data: decks_schema.DeckCreate) -> Any:
    instance = models.Deck(**data.dict())
    await instance.save()
    return instance


@router.get("/decks/{deck_id}/cards/", response_model=decks_schema.Cards)
async def list_cards(deck_id: int) -> Any:
    objects = await models.Card.filter({"deck_id": deck_id})
    return {"items": objects}


@router.get("/cards/{card_id}/", response_model=decks_schema.Card)
async def get_card(card_id: UUID) -> Any:
    instance = await models.Card.get_by_id(card_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Card is not found")
    return instance


@router.post("/decks/{deck_id}/cards/", response_model=decks_schema.Cards)
async def create_cards(deck_id: int, data: List[decks_schema.CardCreate]) -> Any:
    async with transaction():
        objects = await models.Card.bulk_create(
            [models.Card(**card.dict(), deck_id=deck_id) for card in data],
        )
    return {"items": objects}


@router.put("/decks/{deck_id}/cards/", response_model=decks_schema.Cards)
async def update_cards(deck_id: int, data: List[decks_schema.Card]) -> Any:
    async with transaction():
        objects = await models.Card.bulk_update(
            [models.Card(**card.dict(exclude={"deck_id"}), deck_id=deck_id) for card in data],
        )
    return {"items": objects}
