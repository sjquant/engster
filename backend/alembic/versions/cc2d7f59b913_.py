"""empty message

Revision ID: cc2d7f59b913
Revises: bfc8bd91458a
Create Date: 2019-03-09 12:26:00.547728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc2d7f59b913'
down_revision = 'bfc8bd91458a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('translation_content_id_fkey', 'translation', type_='foreignkey')
    op.drop_column('translation', 'content_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('translation', sa.Column('content_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('translation_content_id_fkey', 'translation', 'content', ['content_id'], ['id'])
    # ### end Alembic commands ###