from src.modules.auth.models import User


class UserRepository:
    async def create_user(
            self,
            username: str,
            email: str,
            password_hash: str,
    ) -> User:
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
        )

        await user.insert()

        return user

    async def get_user_by_email(
            self,
            email: str
    ) -> User | None:
        return await User.find_one(User.email == email)
