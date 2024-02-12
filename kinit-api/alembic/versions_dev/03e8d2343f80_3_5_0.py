"""3.5.0

Revision ID: 03e8d2343f80
Revises: dda01c81d162
Create Date: 2024-02-12 07:12:12.009916

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '03e8d2343f80'
down_revision = 'dda01c81d162'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vadmin_auth_dept', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_dept', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.create_foreign_key(None, 'vadmin_auth_dept', 'vadmin_auth_dept', ['parent_id'], ['id'], ondelete='CASCADE')
    op.alter_column('vadmin_auth_menu', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_menu', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.create_foreign_key(None, 'vadmin_auth_menu', 'vadmin_auth_menu', ['parent_id'], ['id'], ondelete='CASCADE')
    op.alter_column('vadmin_auth_role', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_role', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.create_foreign_key(None, 'vadmin_auth_role_depts', 'vadmin_auth_dept', ['dept_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'vadmin_auth_role_depts', 'vadmin_auth_role', ['role_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'vadmin_auth_role_menus', 'vadmin_auth_menu', ['menu_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'vadmin_auth_role_menus', 'vadmin_auth_role', ['role_id'], ['id'], ondelete='CASCADE')
    op.alter_column('vadmin_auth_user', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_user', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.create_foreign_key(None, 'vadmin_auth_user_depts', 'vadmin_auth_dept', ['dept_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'vadmin_auth_user_depts', 'vadmin_auth_user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'vadmin_auth_user_roles', 'vadmin_auth_user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'vadmin_auth_user_roles', 'vadmin_auth_role', ['role_id'], ['id'], ondelete='CASCADE')
    op.alter_column('vadmin_help_issue', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_help_issue', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.create_foreign_key(None, 'vadmin_help_issue', 'vadmin_help_issue_category', ['category_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'vadmin_help_issue', 'vadmin_auth_user', ['create_user_id'], ['id'], ondelete='RESTRICT')
    op.alter_column('vadmin_help_issue_category', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_help_issue_category', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.create_foreign_key(None, 'vadmin_help_issue_category', 'vadmin_auth_user', ['create_user_id'], ['id'], ondelete='RESTRICT')
    op.alter_column('vadmin_record_login', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_login', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_sms_send', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_sms_send', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.create_foreign_key(None, 'vadmin_record_sms_send', 'vadmin_auth_user', ['user_id'], ['id'], ondelete='CASCADE')
    op.alter_column('vadmin_resource_images', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_resource_images', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.create_foreign_key(None, 'vadmin_resource_images', 'vadmin_auth_user', ['create_user_id'], ['id'], ondelete='RESTRICT')
    op.alter_column('vadmin_system_dict_details', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_dict_details', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.create_foreign_key(None, 'vadmin_system_dict_details', 'vadmin_system_dict_type', ['dict_type_id'], ['id'], ondelete='CASCADE')
    op.alter_column('vadmin_system_dict_type', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_dict_type', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_settings', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_settings', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.create_foreign_key(None, 'vadmin_system_settings', 'vadmin_system_settings_tab', ['tab_id'], ['id'], ondelete='CASCADE')
    op.alter_column('vadmin_system_settings_tab', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_settings_tab', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vadmin_system_settings_tab', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_settings_tab', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.drop_constraint(None, 'vadmin_system_settings', type_='foreignkey')
    op.alter_column('vadmin_system_settings', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_settings', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_dict_type', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_dict_type', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.drop_constraint(None, 'vadmin_system_dict_details', type_='foreignkey')
    op.alter_column('vadmin_system_dict_details', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_dict_details', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.drop_constraint(None, 'vadmin_resource_images', type_='foreignkey')
    op.alter_column('vadmin_resource_images', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_resource_images', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.drop_constraint(None, 'vadmin_record_sms_send', type_='foreignkey')
    op.alter_column('vadmin_record_sms_send', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_sms_send', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_login', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_login', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.drop_constraint(None, 'vadmin_help_issue_category', type_='foreignkey')
    op.alter_column('vadmin_help_issue_category', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_help_issue_category', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.drop_constraint(None, 'vadmin_help_issue', type_='foreignkey')
    op.drop_constraint(None, 'vadmin_help_issue', type_='foreignkey')
    op.alter_column('vadmin_help_issue', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_help_issue', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.drop_constraint(None, 'vadmin_auth_user_roles', type_='foreignkey')
    op.drop_constraint(None, 'vadmin_auth_user_roles', type_='foreignkey')
    op.drop_constraint(None, 'vadmin_auth_user_depts', type_='foreignkey')
    op.drop_constraint(None, 'vadmin_auth_user_depts', type_='foreignkey')
    op.alter_column('vadmin_auth_user', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_user', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.drop_constraint(None, 'vadmin_auth_role_menus', type_='foreignkey')
    op.drop_constraint(None, 'vadmin_auth_role_menus', type_='foreignkey')
    op.drop_constraint(None, 'vadmin_auth_role_depts', type_='foreignkey')
    op.drop_constraint(None, 'vadmin_auth_role_depts', type_='foreignkey')
    op.alter_column('vadmin_auth_role', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_role', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.drop_constraint(None, 'vadmin_auth_menu', type_='foreignkey')
    op.alter_column('vadmin_auth_menu', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_menu', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.drop_constraint(None, 'vadmin_auth_dept', type_='foreignkey')
    op.alter_column('vadmin_auth_dept', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_dept', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    # ### end Alembic commands ###
