"""Alters Ticket ticket_numbers table to numbers.

Revision ID: 07d1b1dcfa20
Revises: f53a7e08664e
Create Date: 2021-04-15 06:39:11.109603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07d1b1dcfa20'
down_revision = 'f53a7e08664e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('numbers', sa.String(), nullable=False))
    op.drop_column('tickets', 'ticket_numbers')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('ticket_numbers', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('tickets', 'numbers')
    # ### end Alembic commands ###
