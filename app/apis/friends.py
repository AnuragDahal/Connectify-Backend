from fastapi import APIRouter, status
from ..handlers.User.Friends.friendhandler import FriendsHandler


router = APIRouter(prefix="/api/v1/friends", tags=["Friends"])


@router.post("/add", status_code=status.HTTP_200_OK)
async def send_friend_request(friend_email: str, user_email: str):
    """Send a friend request to the user."""

    response = FriendsHandler.HandleFriendRequest(friend_email, user_email)
    return response


@router.post("/accept", status_code=status.HTTP_200_OK)
async def accept_friend_request(friend_email: str, user_email: str):
    """Accept the friend request from the user."""

    response = FriendsHandler.HandleFriendAcceptance(friend_email, user_email)
    return response


@router.get("/", status_code=status.HTTP_200_OK)
async def show_friends(email: str):
    """Show all the friends of the user."""

    response = FriendsHandler.HandleShowFriends(email)
    return response


@router.get("/requests", status_code=status.HTTP_200_OK)
async def show_friend_requests(email: str):
    """Show all the friend requests of the user."""

    response = FriendsHandler.HandleShowFriendRequests(email)
    return response
