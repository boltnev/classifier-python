"""initial db

Revision ID: 527df7c05433
Revises: None
Create Date: 2013-09-19 22:35:28.089376

"""

# revision identifiers, used by Alembic.
revision = '527df7c05433'
down_revision = None

from alembic import op
import sqlalchemy as sa
Column = sa.Column
VARCHARL = 128

def upgrade():
    op.create_table(
        'documents',
        Column('id', sa.Integer, primary_key=True),
        Column('text', sa.Text),
        Column('category', sa.String(VARCHARL), index=True),
        Column('title', sa.String(VARCHARL), index=True ),
        Column('author', sa.String(VARCHARL), index=True),
        Column('date', sa.String(VARCHARL), index=True),
        Column('indexed', sa.Boolean, default=False, index=True), 
        Column('word_count', sa.Integer, index=True),
        Column('uniq_words', sa.Integer, index=True),
        Column('doc_type', sa.String(VARCHARL), index=True),
        Column('locked', sa.Boolean, default=False)
    )
    
    op.create_table(
        'words',
        Column('id', sa.Integer, primary_key=True),
        Column('word', sa.String(VARCHARL / 4), index=True, unique=True),
        Column('count', sa.Integer, default=1, index=True),
    )
    
    op.create_table(
        'word_features',
        Column('id', sa.Integer, primary_key=True),
        Column('word_id', sa.Integer, sa.ForeignKey('words.id'), index=True),  
        Column('document_id',sa.Integer, sa.ForeignKey('documents.id'), index=True)
    )


def downgrade():
    op.drop_table('word_features')
    op.drop_table('words')
    op.drop_table('documents')
    
