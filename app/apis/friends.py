from fastapi import APIRouter, status, Depends
from ..handlers.User.Friends.friendhandler import FriendsHandler
from ..config.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/friends", tags=["Friends"],
                   dependencies=[Depends(get_current_user)])


@router.post("/add", status_code=status.HTTP_200_OK)
async def send_friend_request(friend_email: str, user_email: str):
    """Send a friend request to the user."""

    response = await FriendsHandler.HandleFriendRequest(friend_email, user_email)
    return response


@router.post("/accept", status_code=status.HTTP_200_OK)
async def accept_friend_request(friend_email: str, user_email: str):
    """Accept the friend request from the user."""

    response = await FriendsHandler.HandleFriendAcceptance(friend_email, user_email)
    return response


@router.get("/", status_code=status.HTTP_200_OK)
async def show_friends(email: str):
    """Show all the friends of the user."""

    response = await FriendsHandler.HandleShowFriends(email)
    return response


@router.get("/requests", status_code=status.HTTP_200_OK)
async def show_friend_requests(email: str):
    """Show all the friend requests of the user."""

    response = await FriendsHandler.HandleShowFriendRequests(email)
    return response


@router.delete("/requests/remove", status_code=status.HTTP_200_OK)
async def remove_friend_requests(friend_email: str, user_email: str):
    """Remove the req from the friend_requests list"""
    response = await FriendsHandler.HandleRemoveFriendRequests(
        friend_email, user_email)
    return response


@router.delete("/remove", status_code=status.HTTP_200_OK)
async def remove_friend(friend_email: str, user_email: str):
    """Remove the friend from the friends list"""
    response = await FriendsHandler.HandleRemoveFriend(friend_email, user_email)
    return response
