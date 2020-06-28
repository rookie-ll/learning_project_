"""empty message

Revision ID: 2b32b2208793
Revises: 4ada326dc9a2
Create Date: 2020-03-07 14:46:12.073584

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2b32b2208793'
down_revision = '4ada326dc9a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book', 'summary',
               existing_type=mysql.VARCHAR(length=1000),
               type_=sa.String(length=3000),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book', 'summary',
               existing_type=sa.String(length=3000),
               type_=mysql.VARCHAR(length=1000),
               existing_nullable=True)
    # ### end Alembic commands ###
