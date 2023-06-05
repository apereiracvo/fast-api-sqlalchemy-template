from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.db.utils import transaction
from app.models.decks_model import CardModel, DeckModel
from app.schemas.decks_schema import Card, CardCreate, Cards, Deck, DeckCreate, Decks


router = APIRouter()


@router.get("/decks/", response_model=Decks)
async def list_decks() -> Any:
    objects = await DeckModel.all()
    return {"items": objects}


@router.get("/decks/{deck_id}/", response_model=Deck)
async def get_deck(deck_id: UUID) -> Any:
    instance = await DeckModel.get_by_id(deck_id, prefetch=("cards",))
    if not instance:
        raise HTTPException(status_code=404, detail="Deck is not found")
    return instance


@router.put("/decks/{deck_id}/", response_model=Deck)
async def update_deck(deck_id: UUID, data: DeckCreate) -> Any:
    instance = await DeckModel.get_by_id(deck_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Deck is not found")
    await instance.update_attrs(**data.dict())
    await instance.save()
    return instance


@router.post("/decks/", response_model=Decks)
async def create_deck(data: DeckCreate) -> Any:
    instance = DeckModel(**data.dict())
    await instance.save()
    return instance


@router.get("/decks/{deck_id}/cards/", response_model=Cards)
async def list_cards(deck_id: int) -> Any:
    objects = await CardModel.filter({"deck_id": deck_id})
    return {"items": objects}


@router.get("/cards/{card_id}/", response_model=Card)
async def get_card(card_id: UUID) -> Any:
    instance = await CardModel.get_by_id(card_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Card is not found")
    return instance


@router.post("/decks/{deck_id}/cards/", response_model=Cards)
async def create_cards(deck_id: int, data: List[CardCreate]) -> Any:
    async with transaction():
        objects = await CardModel.bulk_create(
            [CardModel(**card.dict(), deck_id=deck_id) for card in data],
        )
    return {"items": objects}


@router.put("/decks/{deck_id}/cards/", response_model=Cards)
async def update_cards(deck_id: int, data: List[CardModel]) -> Any:
    async with transaction():
        objects = await CardModel.bulk_update(
            [CardModel(**card.dict(exclude={"deck_id"}), deck_id=deck_id) for card in data],
        )
    return {"items": objects}
