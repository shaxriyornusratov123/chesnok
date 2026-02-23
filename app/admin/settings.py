from starlette_admin.contrib.sqla import Admin

from app.database import engine
from app.models import User,Post,Category,Tag,Profession,Media,Comment
from app.admin.views import UserAdminView,PostAdminView,CategoryAdminView,TagAdminView,ProfessionAdminView,MediaAdminView,CommentAdminView

admin=Admin(engine=engine,title="Chesnok admin", base_url="/admin")
admin.add_view(UserAdminView(User, icon="fa fa-user"))
admin.add_view(PostAdminView(Post,icon="fa fa-video"))
admin.add_view(CategoryAdminView(Category,icon="fa fa-folder"))
admin.add_view(TagAdminView(Tag,icon="fa fa-tag"))
admin.add_view(ProfessionAdminView(Profession, icon="fa fa-briefcase"))
admin.add_view(MediaAdminView(Media,icon="fa fa-image"))
admin.add_view(CommentAdminView(Comment,icon="fa fa-comment")) 