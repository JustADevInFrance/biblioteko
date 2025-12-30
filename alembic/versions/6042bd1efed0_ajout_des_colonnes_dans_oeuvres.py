"""Ajout des colonnes dans oeuvres

Revision ID: 6042bd1efed0
Revises: 
Create Date: 2025-12-15 00:02:45.471023
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6042bd1efed0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    # Étape 1 : ajouter les colonnes
    with op.batch_alter_table("oeuvres") as batch_op:
        batch_op.add_column(sa.Column('format_oeuvre', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('contenu_markdown', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('est_explicite', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('libre_de_droit', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('utilisateur_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('date_creation', sa.DateTime(), nullable=True))

    # Étape 2 : ajouter la contrainte FK dans un batch séparé
    with op.batch_alter_table("oeuvres") as batch_op:
        batch_op.create_foreign_key(
            "fk_oeuvres_utilisateur",  # nom de la contrainte
            "utilisateurs",            # table référencée
            ["utilisateur_id"],        # colonnes locales
            ["id"]                     # colonnes référencées
        )


def downgrade() -> None:
    """Downgrade schema."""
    # Étape 1 : supprimer la FK
    with op.batch_alter_table("oeuvres") as batch_op:
        batch_op.drop_constraint("fk_oeuvres_utilisateur", type_='foreignkey')

    # Étape 2 : supprimer les colonnes
    with op.batch_alter_table("oeuvres") as batch_op:
        batch_op.drop_column('date_creation')
        batch_op.drop_column('utilisateur_id')
        batch_op.drop_column('libre_de_droit')
        batch_op.drop_column('est_explicite')
        batch_op.drop_column('contenu_markdown')
        batch_op.drop_column('format_oeuvre')
