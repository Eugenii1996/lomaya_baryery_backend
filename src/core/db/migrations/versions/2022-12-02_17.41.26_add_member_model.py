"""add_member_model

Revision ID: b681bd3175cc
Revises: b77d14a09655
Create Date: 2022-12-02 17:41:26.789811

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b681bd3175cc'
down_revision = 'b77d14a09655'
branch_labels = None
depends_on = None

MEMBER_STATUS_TYPE = sa.Enum('active', 'excluded', name='member_status')
MEMBER_STATUS_TYPE_PG = postgresql.ENUM('active', 'excluded', name='member_status', create_type=False)
MEMBER_STATUS_TYPE.with_variant(MEMBER_STATUS_TYPE_PG, 'postgresql')


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('members',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('status', MEMBER_STATUS_TYPE, nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('shift_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('numbers_lombaryers', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['shift_id'], ['shifts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'shift_id', name='_user_shift_uc')
    )
    op.add_column('user_tasks', sa.Column('member_id', postgresql.UUID(as_uuid=True), nullable=False))
    op.drop_constraint('_user_task_uc', 'user_tasks', type_='unique')
    op.create_unique_constraint('_member_task_uc', 'user_tasks', ['shift_id', 'task_date', 'member_id'])
    op.drop_constraint('user_tasks_user_id_fkey', 'user_tasks', type_='foreignkey')
    op.create_foreign_key('user_tasks_member_id_fkey', 'user_tasks', 'members', ['member_id'], ['id'])
    op.drop_column('user_tasks', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_tasks', sa.Column('user_id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint('user_tasks_member_id_fkey', 'user_tasks', type_='foreignkey')
    op.create_foreign_key('user_tasks_user_id_fkey', 'user_tasks', 'users', ['user_id'], ['id'])
    op.drop_constraint('_member_task_uc', 'user_tasks', type_='unique')
    op.create_unique_constraint('_user_task_uc', 'user_tasks', ['user_id', 'shift_id', 'task_date'])
    op.drop_column('user_tasks', 'member_id')
    op.drop_table('members')
    MEMBER_STATUS_TYPE.drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###
