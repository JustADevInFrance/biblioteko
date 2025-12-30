"""Ajout des colonnes manquantes dans oeuvres

Revision ID: 249f47dd5fdc
Revises: 6042bd1efed0
Create Date: 2025-12-15 00:12:11.425060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '249f47dd5fdc'
down_revision: Union[str, Sequence[str], None] = '6042bd1efed0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
