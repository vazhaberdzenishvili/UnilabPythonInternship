from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import UserModel, StoreModel, Role, UserRoles
from app.database import db
from flask import redirect, url_for, request
from flask_login import current_user

admin = Admin(name='Panel', template_mode='bootstrap4')


class UserModelView(ModelView):
    column_exclude_list = ['password', ]

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('UserModel.login', next=request.url))


# class AdminModelView(ModelView):
#     column_exclude_list = ['password', ]
#
#     def is_accessible(self):
#         if current_user.is_authenticated:
#             if current_user.Status == '1':
#                 return True
#
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('UserModel.login', next=request.url))


admin.add_view(UserModelView(UserModel, db.session))
# admin.add_view(ModelView(StoreModel, db.session))
admin.add_view(ModelView(StoreModel, db.session, name="Store"))
admin.add_view(ModelView(Role, db.session, name="UserRoles"))
