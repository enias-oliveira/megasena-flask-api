"""Creates TicketModel.

Revision ID: f53a7e08664e
Revises: 28bbf10e12cd
Create Date: 2021-04-15 02:02:23.136455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f53a7e08664e'
down_revision = '28bbf10e12cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tickets',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('ticket_numbers', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tickets')
    # ### end Alembic commands ###
