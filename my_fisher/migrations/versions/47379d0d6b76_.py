"""empty message

Revision ID: 47379d0d6b76
Revises: 13269f41a472
Create Date: 2020-03-03 11:14:45.935940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47379d0d6b76'
down_revision = '13269f41a472'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('status', sa.SmallInteger(), nullable=True))
    op.add_column('gift', sa.Column('status', sa.SmallInteger(), nullable=True))
    op.add_column('user', sa.Column('status', sa.SmallInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'status')
    op.drop_column('gift', 'status')
    op.drop_column('book', 'status')
    # ### end Alembic commands ###
