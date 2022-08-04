"""empty message

Revision ID: 602dfaeaed1f
Revises: a7b5e71bd728
Create Date: 2022-08-04 21:51:36.181661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '602dfaeaed1f'
down_revision = 'a7b5e71bd728'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Artist_show_id_fkey', 'Artist', type_='foreignkey')
    op.drop_column('Artist', 'show_id')
    op.add_column('Shows', sa.Column('artist_id', sa.Integer(), nullable=True))
    op.add_column('Shows', sa.Column('venue_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Shows', 'Artist', ['artist_id'], ['id'])
    op.create_foreign_key(None, 'Shows', 'Venue', ['venue_id'], ['id'])
    op.drop_constraint('Venue_show_id_fkey', 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'show_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('show_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('Venue_show_id_fkey', 'Venue', 'Shows', ['show_id'], ['id'])
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.drop_column('Shows', 'venue_id')
    op.drop_column('Shows', 'artist_id')
    op.add_column('Artist', sa.Column('show_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('Artist_show_id_fkey', 'Artist', 'Shows', ['show_id'], ['id'])
    # ### end Alembic commands ###
