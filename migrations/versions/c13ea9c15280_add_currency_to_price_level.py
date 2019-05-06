"""Add currency to price level

Revision ID: c13ea9c15280
Revises: 5346190a2f75
Create Date: 2019-04-30 20:08:08.487672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c13ea9c15280'
down_revision = '5346190a2f75'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('price_level', sa.Column('currency', sa.String(length=3), default="USD"))

def downgrade():
    op.drop_column('price_level', 'currency')
