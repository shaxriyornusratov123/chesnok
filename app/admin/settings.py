from starlette_admin.contrib.sqla import Admin

from app.database import engine
from app.models import User,Post
from app.admin.views import UserAdminView,PostAdminView

admin=Admin(engine=engine,title="Chesnok admin", base_url="/admin")
admin.add_view(UserAdminView(User, icon="fa fa-user"))
admin.add_view(PostAdminView(Post,icon="fa fa-post"))