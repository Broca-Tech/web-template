from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.application.services.user_service import UserService
from app.infrastructure.database.base import get_db
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.presentation.dto.user_dto import UserCreate, UserUpdate, UserResponse
from app.shared.exceptions import UserNotFoundError, UserAlreadyExistsError

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency to get user service"""
    user_repository = UserRepositoryImpl(db)
    return UserService(user_repository)


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0, 
    limit: int = 100, 
    user_service: UserService = Depends(get_user_service)
):
    """Get all users"""
    users = await user_service.get_all_users(skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int, 
    user_service: UserService = Depends(get_user_service)
):
    """Get user by ID"""
    try:
        user = await user_service.get_user_by_id(user_id)
        return UserResponse.model_validate(user)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, 
    user_service: UserService = Depends(get_user_service)
):
    """Create new user"""
    try:
        created_user = await user_service.create_user(
            email=user.email,
            username=user.username,
            password=user.password
        )
        return UserResponse.model_validate(created_user)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, 
    user: UserUpdate, 
    user_service: UserService = Depends(get_user_service)
):
    """Update user"""
    try:
        update_data = user.model_dump(exclude_unset=True)
        updated_user = await user_service.update_user(user_id, **update_data)
        return UserResponse.model_validate(updated_user)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, 
    user_service: UserService = Depends(get_user_service)
):
    """Delete user"""
    try:
        await user_service.delete_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    user_id: int, 
    user_service: UserService = Depends(get_user_service)
):
    """Deactivate user"""
    try:
        user = await user_service.deactivate_user(user_id)
        return UserResponse.model_validate(user)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: int, 
    user_service: UserService = Depends(get_user_service)
):
    """Activate user"""
    try:
        user = await user_service.activate_user(user_id)
        return UserResponse.model_validate(user)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) 