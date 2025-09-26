from typing import List, Optional
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.shared.exceptions import UserNotFoundError, UserAlreadyExistsError


class UserService:
    """User application service"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def create_user(self, email: str, username: str, password: str) -> User:
        """Create a new user"""
        # Check if user already exists
        if await self.user_repository.exists_by_email(email):
            raise UserAlreadyExistsError(f"User with email {email} already exists")
        
        if await self.user_repository.exists_by_username(username):
            raise UserAlreadyExistsError(f"User with username {username} already exists")
        
        # Create user entity
        user = User(
            id=None,
            email=email,
            username=username,
            hashed_password=password  # In production, this should be hashed
        )
        
        return await self.user_repository.create(user)
    
    async def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        return user
    
    async def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise UserNotFoundError(f"User with email {email} not found")
        return user
    
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return await self.user_repository.get_all(skip=skip, limit=limit)
    
    async def update_user(self, user_id: int, **kwargs) -> User:
        """Update user"""
        user = await self.get_user_by_id(user_id)
        
        # Update user attributes
        user.update(**kwargs)
        
        return await self.user_repository.update(user)
    
    async def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        user = await self.get_user_by_id(user_id)
        return await self.user_repository.delete(user_id)
    
    async def deactivate_user(self, user_id: int) -> User:
        """Deactivate user"""
        user = await self.get_user_by_id(user_id)
        user.deactivate()
        return await self.user_repository.update(user)
    
    async def activate_user(self, user_id: int) -> User:
        """Activate user"""
        user = await self.get_user_by_id(user_id)
        user.activate()
        return await self.user_repository.update(user) 