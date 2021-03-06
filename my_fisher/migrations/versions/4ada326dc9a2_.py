"""empty message

Revision ID: 4ada326dc9a2
Revises: 47379d0d6b76
Create Date: 2020-03-07 14:36:26.756964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ada326dc9a2'
down_revision = '47379d0d6b76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wish',
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('isbn', sa.String(length=15), nullable=False),
    sa.Column('launched', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wish')
    # ### end Alembic commands ###
