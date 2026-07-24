"""initial_schema

Revision ID: 001_initial
Revises: 
Create Date: 2026-07-24 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('firebase_uid', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('firebase_uid')
    )
    op.create_index(op.f('ix_users_firebase_uid'), 'users', ['firebase_uid'], unique=True)

    op.create_table(
        'projects',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('preview_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'tasks',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('project_id', sa.String(), nullable=False),
        sa.Column('task_key', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('agent_role', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('dependencies', sa.JSON(), nullable=True),
        sa.Column('task_metadata', sa.JSON(), nullable=True),
        sa.Column('output', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'agent_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('project_id', sa.String(), nullable=False),
        sa.Column('agent_role', sa.String(), nullable=False),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('log_data', sa.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'project_files',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('project_id', sa.String(), nullable=False),
        sa.Column('path', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('project_files')
    op.drop_table('agent_logs')
    op.drop_table('tasks')
    op.drop_table('projects')
    op.drop_table('users')
