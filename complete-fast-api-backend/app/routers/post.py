from typing import List, Optional

from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

import app.models as models
from app.database import get_db
from app.schemas import PostCreate, PostResponse
from app.oauth2 import get_current_user

router = APIRouter(prefix="/sqlalchemy/posts", tags=["Posts"])


@router.get("", response_model=List[PostResponse])
async def get_sqlalchemy_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.user_id == current_user.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
    )
    return posts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_new_sql_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    # new_post = models.Post(title=post.title, content=post.content,
    #                        published=post.published)
    print(current_user.email)
    post_dict = post.dict()
    post_dict.pop("rating", None)
    # adding user
    new_post = models.Post(user_id=current_user.id, **post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # this block is not getting executed anymore
    return new_post


# title sr, content str


@router.get("/{id}", response_model=PostResponse)
def get_sqlalchemy_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    test_post = db.query(models.Post).filter(models.Post.id == id).first()
    # cursor.execute("""SELECT * FROM posts where id=%s""", (str(id),))
    # test_post = cursor.fetchone()
    # post = find_post(id)
    print(test_post)
    if not test_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return test_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sqlalchemy_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    # post_index = find_post_index(id)
    deleted_query = db.query(models.Post).filter(models.Post.id == id)

    delete_post = deleted_query.first()

    if deleted_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    if delete_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    # my_posts.pop(post_index)
    deleted_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostResponse)
def sql_update_post(
    id: int,
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    update_query = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute("""UPDATE posts SET title=%s,content=%s, published=%s
    #                WHERE id=%s RETURNING *""", (post.title, post.content,
    #                                             post.published, str(id)))
    # post_index = find_post_index(id)
    post_dict = post.dict()
    del post_dict["rating"]
    post_res = update_query.first()
    if post_res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    if post_res.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    update_query.update(post_dict, synchronize_session=False)
    db.commit()
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[post_index] = post_dict
    return update_query.first()
