"""empty message

Revision ID: 633bff0ab96f
Revises: 
Create Date: 2019-04-26 23:28:20.821013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '633bff0ab96f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userprofile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('biography', sa.Text(), nullable=False),
    sa.Column('profile_photo', sa.String(length=200), nullable=True),
    sa.Column('joined_on', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('follow',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['follower_id'], ['userprofile.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['userprofile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('photo', sa.String(), nullable=True),
    sa.Column('caption', sa.Text(), nullable=True),
    sa.Column('created_on', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['userprofile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['userprofile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    op.drop_table('post')
    op.drop_table('follow')
    op.drop_table('userprofile')
    # ### end Alembic commands ###
