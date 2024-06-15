"""empty message

Revision ID: b496d41b2524
Revises: 1e846fcc471e
Create Date: 2024-06-14 23:36:29.511008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b496d41b2524'
down_revision: Union[str, None] = '1e846fcc471e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('types', sa.Column('pokemon_id', sa.Integer(), nullable=False))
    op.create_foreign_key(op.f('fk_types_pokemon_id_pokemons'), 'types', 'pokemons', ['pokemon_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_types_pokemon_id_pokemons'), 'types', type_='foreignkey')
    op.drop_column('types', 'pokemon_id')
    # ### end Alembic commands ###
