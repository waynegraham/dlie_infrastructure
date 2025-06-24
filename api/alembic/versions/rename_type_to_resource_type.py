"""
Rename the 'type' column on resources to 'resource_type'.

Revision ID: rename_type_to_resource_type
Revises: 
Create Date: 2024-04-19 00:00:00.000000
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'rename_type_to_resource_type'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column(
        'resources',
        'type',
        new_column_name='resource_type',
    )

def downgrade():
    op.alter_column(
        'resources',
        'resource_type',
        new_column_name='type',
    )