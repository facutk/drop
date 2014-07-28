"""empty message

Revision ID: 59afa21b8e56
Revises: 34e8fb3c02b7
Create Date: 2014-07-22 14:40:53.203000

"""

# revision identifiers, used by Alembic.
revision = '59afa21b8e56'
down_revision = '34e8fb3c02b7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('counter', sa.Column('images', sa.Text(), nullable=True))
    op.add_column('counter', sa.Column('mail', sa.String(length=32), nullable=True))
    op.add_column('counter', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.add_column('counter', sa.Column('sequences', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('counter', 'sequences')
    op.drop_column('counter', 'password_hash')
    op.drop_column('counter', 'mail')
    op.drop_column('counter', 'images')
    ### end Alembic commands ###