"""add_sequence_number_and_tasks_to_shift

Revision ID: b77d14a09655
Revises: 1d0b63b24b19
Create Date: 2022-12-01 11:16:13.521755

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b77d14a09655'
down_revision = '1d0b63b24b19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shifts', sa.Column('sequence_number', sa.Integer(), sa.Identity(always=False, start=1, cycle=True), nullable=False))
    op.add_column('shifts', sa.Column('tasks', sa.JSON(), nullable=True))
    op.execute("UPDATE shifts SET tasks='{}'")
    op.alter_column('shifts', 'tasks', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shifts', 'tasks')
    op.drop_column('shifts', 'sequence_number')
    # ### end Alembic commands ###
