"""empty message

Revision ID: 5346190a2f75
Revises: a908fb8b1d23
Create Date: 2019-01-28 03:05:26.706536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5346190a2f75'
down_revision = 'a908fb8b1d23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_payment', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_payment')
    # ### end Alembic commands ###