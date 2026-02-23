from starlette_admin.contrib.sqla  import Admin 


from app.database import engine
from app.models import User


admin=Admin(engine=engine, title="Chesnok admin", base_url="/admin")

