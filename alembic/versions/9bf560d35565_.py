"""empty message

Revision ID: 9bf560d35565
Revises: c5dc02c95676
Create Date: 2020-03-01 23:48:22.423370

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "9bf560d35565"
down_revision = "c5dc02c95676"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("translation", "translator_id", new_column_name="user_id")
    op.drop_constraint(
        "translation_translator_id_fkey", "translation", type_="foreignkey"
    )
    op.create_foreign_key(
        "translation_user_id_fkey", "translation", "user", ["user_id"], ["id"],
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("translation", "user_id", new_column_name="translator_id")
    op.drop_constraint(
        "translation_translator_id_fkey", "translation", type_="foreignkey"
    )
    op.create_foreign_key(
        "translation_translator_id_fkey",
        "translation",
        "user",
        ["translator_id"],
        ["id"],
    )
    # ### end Alembic commands ###
