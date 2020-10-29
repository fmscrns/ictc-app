"""empty message

Revision ID: ab9846fb58f4
Revises: 06f93592e36a
Create Date: 2020-10-26 12:14:29.415495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab9846fb58f4'
down_revision = '06f93592e36a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mode', sa.Column('registered_on', sa.DateTime(), nullable=False))
    op.add_column('nature', sa.Column('registered_on', sa.DateTime(), nullable=False))
    op.add_column('office', sa.Column('registered_on', sa.DateTime(), nullable=False))
    op.add_column('repair', sa.Column('registered_on', sa.DateTime(), nullable=False))
    op.add_column('request', sa.Column('registered_on', sa.DateTime(), nullable=False))
    op.add_column('technician', sa.Column('registered_on', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('technician', 'registered_on')
    op.drop_column('request', 'registered_on')
    op.drop_column('repair', 'registered_on')
    op.drop_column('office', 'registered_on')
    op.drop_column('nature', 'registered_on')
    op.drop_column('mode', 'registered_on')
    # ### end Alembic commands ###