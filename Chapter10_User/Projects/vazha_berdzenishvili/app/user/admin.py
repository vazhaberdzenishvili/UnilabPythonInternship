from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import UserModel,Role, UserRoles
from app.database import db
from flask import redirect, url_for, request
from flask_user import current_user
from app.models.store import StoreModel

admin = Admin(name='Panel', template_mode='bootstrap4')


class UserModelView(ModelView):
    column_exclude_list = ['password', ]

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('UserModel.login', next=request.url))


class AdminModelView(ModelView):
    column_exclude_list = ['password', ]

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.has_role("Admin")

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('UserModel.login', next=request.url))


admin.add_view(AdminModelView(UserModel, db.session))
admin.add_view(UserModelView(StoreModel, db.session))
admin.add_view(UserModelView(Role, db.session, name="User Roles"))
