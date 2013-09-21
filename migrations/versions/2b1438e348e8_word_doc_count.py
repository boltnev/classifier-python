"""word doc_count

Revision ID: 2b1438e348e8
Revises: 3a43d98486a2
Create Date: 2013-09-22 00:59:18.086613

"""

# revision identifiers, used by Alembic.
revision = '2b1438e348e8'
down_revision = '3a43d98486a2'

from alembic import op
import sqlalchemy as sa


def upgrade():
     op.add_column('words', sa.Column('doc_count', sa.Integer))  


def downgrade():
    op.drop_column('words', 'doc_count')  
