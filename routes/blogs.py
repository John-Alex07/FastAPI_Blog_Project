from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from models.user import User, BlogPost
from config.database import db
from routes.authentication import get_current_user
from fastapi import Query
from datetime import datetime

blogs = APIRouter()

# Route to create a new blog post
@blogs.post("/blogs/", response_model=BlogPost)
async def create_blog(blog: BlogPost, current_user: User = Depends(get_current_user)):
    blog_dict = blog.dict()
    blog_dict["author"] = current_user["username"]
    blog_dict["created_at"] = datetime.now()
    blog_id = await db["Blogs"].insert_one(blog_dict)
    created_blog = await db["Blogs"].find_one({"_id": blog_id.inserted_id})
    return created_blog

# Route to retrieve all blog posts
@blogs.get("/blogs/", response_model=List[BlogPost])
async def get_all_blogs(page: int = Query(default=1, ge=1), page_size: int = Query(default=10, le=100), sort_by: str = Query(default="created_at", description="Field to sort by"), sort_order: str = Query(default="desc", description="Sort order (asc or desc)")):
    sort_order = 1 if sort_order.lower() == "asc" else -1
    skip = (page - 1) * page_size
    blogs = await db["Blogs"].find().sort(sort_by, sort_order).skip(skip).limit(page_size).to_list(length=None)
    return blogs

# # Route to retrieve a specific blog post by ID
# @blogs.get("/blogs/{blog_id}", response_model=BlogPost)
# async def get_blog_by_id(blog_id: str,):
#     blog = await db["Blogs"].find_one({"_id": ObjectId(blog_id)})
#     if blog:
#         return blog
#     else:
#         raise HTTPException(status_code=404, detail="Blog not found")

#Route to retrieve blog id by title
@blogs.get("/blogs/{title}", response_model=BlogPost)
async def get_blog_by_title(title: str):
    blog = await db["Blogs"].find_one({"title": title})
    if blog:
        return blog
    else:
        raise HTTPException(status_code=404, detail="Blog not found")


#Route to update a blog post by title
@blogs.put("/blogs/{title}", response_model=BlogPost)
async def update_blog_by_title(title: str, blog: BlogPost, current_user: User = Depends(get_current_user)):
    existing_blog = await db["Blogs"].find_one({"title":
    title})
    if not existing_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if existing_blog["author"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="You are not the author of this blog post")
    blog_dict = blog.dict()
    blog_dict["author"] = current_user["username"]
    blog_dict["created_at"] = datetime.now()
    await db["Blogs"].update_one({"title": title}, {"$set": blog_dict})
    updated_blog = await db["Blogs"].find_one({"title": title})
    return updated_blog

# # Route to update a blog post
# @blogs.put("/blogs/{blog_id}", response_model=BlogPost)
# async def update_blog(blog_id: str, blog: BlogPost, current_user: User = Depends(get_current_user)):
#     existing_blog = await db["Blogs"].find_one({"_id": ObjectId(blog_id)})
#     if not existing_blog:
#         raise HTTPException(status_code=404, detail="Blog not found")
#     if existing_blog["author"] != current_user["username"]:
#         raise HTTPException(status_code=403, detail="You are not the author of this blog post")
#     await db["Blogs"].update_one({"_id": ObjectId(blog_id)}, {"$set": blog.dict()})
#     updated_blog = await db["Blogs"].find_one({"_id": ObjectId(blog_id)})
#     return updated_blog

# # Route to delete a blog post
# @blogs.delete("/blogs/{blog_id}")
# async def delete_blog(blog_id: str, current_user: User = Depends(get_current_user)):
#     existing_blog = await db["Blogs"].find_one({"_id": ObjectId(blog_id)})
#     if not existing_blog:
#         raise HTTPException(status_code=404, detail="Blog not found")
#     if existing_blog["author"] != current_user["username"]:
#         raise HTTPException(status_code=403, detail="You are not the author of this blog post")
#     await db["Blogs"].delete_one({"_id": ObjectId(blog_id)})
#     return {"message": "Blog deleted successfully"}

# Route to delete a blog post by title
@blogs.delete("/blogs/{title}")
async def delete_blog_by_title(title: str, current_user: User = Depends(get_current_user)):
    existing_blog = await db["Blogs"].find_one({"title":
    title})
    if not existing_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if existing_blog["author"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="You are not the author of this blog post")
    await db["Blogs"].delete_one({"title": title})
    return {"message": "Blog deleted successfully"}

# Getting blogs by tags relevant to the user
@blogs.get("/blogs/tags", response_model=List[BlogPost])
async def get_blogs_by_tags(current_user: User = Depends(get_current_user)):
    tags_relevant = current_user["tags"]
    blogs = await db["Blogs"].find({"tags": {"$in": tags_relevant}}).to_list(length=None)
    return blogs