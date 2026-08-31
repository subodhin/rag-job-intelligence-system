from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.context.context_service import (
    create_user,
    get_user,
    save_profile,
    get_profile,
    save_preferences,
    get_preferences,
    save_message,
    get_conversation
)

from app.context.context_service import (
    create_user,
    get_user,
    save_profile,
    get_profile,
    save_preferences,
    get_preferences,
    save_message,
    get_conversation,
    get_user_context
)

from app.context.context_service import (
    create_user,
    get_user,
    save_profile,
    get_profile,
    save_preferences,
    get_preferences,
    save_message,
    get_conversation,
    get_user_context,
    delete_profile,
    delete_preferences,
    delete_conversation,
    delete_user_context
)


router = APIRouter(
    prefix="/context",
    tags=["Context"]
)


class UserRequest(BaseModel):
    user_id: str


class ProfileRequest(BaseModel):
    target_role: str = None
    experience_level: str = None
    skills: str = None


class PreferencesRequest(BaseModel):
    remote_only: bool = False
    preferred_locations: str = None
    preferred_skills: str = None


class MessageRequest(BaseModel):
    role: str
    content: str


@router.post("/users")
def create_context_user(request: UserRequest):

    print(f"Creating user with ID::::::::::::::::::::::: {request.user_id}")

    create_user(request.user_id)

    return {
        "message": "User created",
        "user_id": request.user_id
    }


@router.get("/users/{user_id}")
def get_context_user(user_id: str):

    print(f"Fetching user with ID::::::::::::::::::::::: {user_id}")

    user = get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/users/{user_id}/profile")
def update_profile(
    
    user_id: str,
    request: ProfileRequest
):

    print(f"Updating profile for user with ID::::::::::::::::::::::: {user_id}")

    save_profile(
        user_id=user_id,
        target_role=request.target_role,
        experience_level=request.experience_level,
        skills=request.skills
    )

    return get_profile(user_id)


@router.get("/users/{user_id}/profile")
def read_profile(user_id: str):

    profile = get_profile(user_id)
    print(f"Fetching profile for user with ID::::::::::::::::::::::: {user_id}")

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile


@router.put("/users/{user_id}/preferences")
def update_preferences(
    user_id: str,
    request: PreferencesRequest
):

    print(f"Updating preferences for user with ID::::::::::::::::::::::: {user_id}") 
    save_preferences(
        user_id=user_id,
        remote_only=request.remote_only,
        preferred_locations=request.preferred_locations,
        preferred_skills=request.preferred_skills
    )

    return get_preferences(user_id)


@router.get("/users/{user_id}/preferences")
def read_preferences(user_id: str):

    preferences = get_preferences(user_id)
    print(f"Fetching preferences for user with ID::::::::::::::::::::::: {user_id}")

    if preferences is None:
        raise HTTPException(
            status_code=404,
            detail="Preferences not found"
        )

    return preferences


@router.post("/users/{user_id}/messages")
def add_message(
    user_id: str,
    request: MessageRequest
):
    print(f"Adding message for user with ID::::::::::::::::::::::: {user_id}")
    if request.role not in ["user", "assistant"]:
        raise HTTPException(
            status_code=400,
            detail="Role must be 'user' or 'assistant'"
        )

    save_message(
        user_id=user_id,
        role=request.role,
        content=request.content
    )

    return {
        "message": "Message saved"
    }


@router.get("/users/{user_id}/messages")
def read_messages(user_id: str):
    print(f"Fetching messages for user with ID::::::::::::::::::::::: {user_id}")

    return get_conversation(user_id)



@router.get("/users/{user_id}/context")
def read_user_context(user_id: str):

    context = get_user_context(user_id)
    print(f"Fetching context for user with ID::::::::::::::::::::::: {user_id}")

    if context is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return context


@router.delete("/users/{user_id}/profile")
def remove_profile(user_id: str):
    print(f"Deleting profile for user with ID::::::::::::::::::::::: {user_id}")

    delete_profile(user_id)

    return {
        "message": "Profile deleted"
    }


@router.delete("/users/{user_id}/preferences")
def remove_preferences(user_id: str):

    print(f"Deleting preferences for user with ID::::::::::::::::::::::: {user_id}")

    delete_preferences(user_id)

    return {
        "message": "Preferences deleted"
    }


@router.delete("/users/{user_id}/messages")
def remove_conversation(user_id: str):
    print(f"Deleting conversation for user with ID::::::::::::::::::::::: {user_id}")

    delete_conversation(user_id)

    return {
        "message": "Conversation deleted"
    }


@router.delete("/users/{user_id}/context")
def remove_user_context(user_id: str):

    print(f"Deleting user context for user with ID::::::::::::::::::::::: {user_id}")

    delete_user_context(user_id)

    return {
        "message": "User context deleted"
    }