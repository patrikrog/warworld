"""empty message

Revision ID: 07520495f4fc
Revises: b28d58ec4299
Create Date: 2023-01-28 14:04:03.812409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07520495f4fc'
down_revision = 'b28d58ec4299'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dead', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('dead')

    # ### end Alembic commands ###
