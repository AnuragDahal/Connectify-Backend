from fastapi import APIRouter, status
from ..handlers.User.Friends.friendhandler import FriendsHandler


router = APIRouter(prefix="/api/v1/friends", tags=["Friends"])


@router.post("/add", status_code=status.HTTP_200_OK)
async def send_friend_request(friend_email: str, user_email: str):
    """Send a friend request to the user."""

    response = FriendsHandler.HandleFriendRequest(friend_email,user_email)
    return response
