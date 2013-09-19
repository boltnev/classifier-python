"""Add a idf to words

Revision ID: 3a43d98486a2
Revises: 527df7c05433
Create Date: 2013-09-19 23:10:33.245059

"""

# revision identifiers, used by Alembic.
revision = '3a43d98486a2'
down_revision = '527df7c05433'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('words', sa.Column('idf', sa.Float))  


def downgrade():
    op.drop_column('words', 'idf')  
    
