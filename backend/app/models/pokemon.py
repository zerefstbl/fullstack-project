from __future__ import annotations

from sqlalchemy import String, Integer, ForeignKey
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Pokemon(Base):
    __tablename__ = "pokemons"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)

    name: Mapped[str] = mapped_column("name", String(length=64), nullable=False)
    front_picture: Mapped[str] = mapped_column("front_picture", String, nullable=True)
    back_picture: Mapped[str] = mapped_column("back_picture", String, nullable=True)
    hp: Mapped[int] = mapped_column("hp", Integer, nullable=False)
    attack: Mapped[int] = mapped_column("attack", Integer, nullable=False)
    defense: Mapped[int] = mapped_column("defense", Integer, nullable=False)
    special_attack: Mapped[int] = mapped_column("special_attack", Integer, nullable=False)
    special_defense: Mapped[int] = mapped_column("special_defense", Integer, nullable=False)
    speed: Mapped[int] = mapped_column("speed", Integer, nullable=False)
    types: Mapped[List[Type]] = relationship("Type", back_populates="pokemon")

class Type(Base):
    __tablename__ = "types"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)

    name: Mapped[str] = mapped_column("name", String(length=64), nullable=False)
    pokemon_id: Mapped[int] = mapped_column("pokemon_id", Integer, ForeignKey('pokemons.id'))  # Chave estrangeira para Pokemon

    pokemon: Mapped[Pokemon] = relationship(
        "Pokemon",
        back_populates="types",
    )
