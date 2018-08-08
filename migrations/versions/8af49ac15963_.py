"""empty message

Revision ID: 8af49ac15963
Revises: d4b983612f6d
Create Date: 2018-07-19 17:02:56.742223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8af49ac15963'
down_revision = 'd4b983612f6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eo_project_status_code_group',
    sa.Column('groupID', sa.Integer(), nullable=False),
    sa.Column('groupName', sa.String(length=255), nullable=False),
    sa.Column('parentGroupID', sa.Integer(), nullable=False),
    sa.Column('isChild', sa.Boolean(), nullable=False),
    sa.Column('projectID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['projectID'], ['eo_project.projectID'], ),
    sa.PrimaryKeyConstraint('groupID')
    )
    op.create_table('eo_project_status_code',
    sa.Column('codeID', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=255), nullable=False),
    sa.Column('codeDescription', sa.String(length=255), nullable=False),
    sa.Column('groupID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['groupID'], ['eo_project_status_code_group.groupID'], ),
    sa.PrimaryKeyConstraint('codeID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eo_project_status_code')
    op.drop_table('eo_project_status_code_group')
    # ### end Alembic commands ###