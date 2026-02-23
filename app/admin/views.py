from starlette_admin.contrib.sqla import ModelView

class UserAdminView(ModelView):
    fields=[
        "id",
        "email",
        "password_hash",
        "first_name",
        "last_name",
        "profession_id",
        "bio",
        "posts_count",
        "posts_read_count",
        "is_active",
        "is_staff",
        "is_superuser",
        "deleted_email",
        "created_at",
        "updated_at"
    ]

    exclude_fields_from_list=[
        "password_hash",
        "bio",
        "posts_count",
        "posts_read_count",
        "is_deleted",
        "deleted_email"
    ]

    exclude_fields_from_detail=[]
    exclude_fields_from_create=[
        "id",
        "created_at",
        "updated_at",
        "posts_count",
        "posts_read_count",
    ]
    exclude_fields_from_edit=["id","password-hash","created_at","updated_at"]

class PostAdminView(ModelView):
    fields=[
        "id",
        "user_id",
        "title",
        "slug",
        "body",
        "category_id",
        "views_count",
        "likes_count",
        "comments_count",
        "mins_read",
        "is_active",
        "created_at",
        "updated_at"
    ]
    
    exclude_fields_from_list=[
        "slug",
        "body",
        "mins_read"
    ]
    exclude_fields_from_detail=[]
    exclude_fields_from_create=[
        "id",
        "user_id"
        "created_at",
        "updated_at",
        "views_count",
        "likes_count",
        
    ]
    exclude_fields_from_edit=[
        "id",
        "user_id",
        "created_at",
        "updated_at"
    ]

