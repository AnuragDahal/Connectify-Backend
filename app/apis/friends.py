from fastapi import APIRouter, status, Query, Form, Depends
from typing import Annotated
from ..handlers.User.Friends.friendhandler import FriendsHandler
from ..config.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/friends", tags=["Friends"], dependencies=[Depends(get_current_user)])


@router.post("/add", status_code=status.HTTP_200_OK)
async def send_friend_request(
    friend_email: Annotated[str, Form(..., description="Email of the friend to add")],
    user_email: Annotated[str, Form(..., description="Email of the current user")]
):
    response = await FriendsHandler.HandleFriendRequest(friend_email, user_email)
    return response


@router.post("/accept", status_code=status.HTTP_200_OK)
async def accept_friend_request(
    friend_email: Annotated[str, Form(..., description="Email of the friend to accept")],
    user_email: Annotated[str, Form(..., description="Email of the current user")]
):
    response = await FriendsHandler.HandleFriendAcceptance(friend_email, user_email)
    return response


@router.get("/", status_code=status.HTTP_200_OK)
async def show_friends(email: Annotated[str, Query(..., description="Email of the user")]):
    response = await FriendsHandler.HandleShowFriends(email)
    return response


@router.get("/requests", status_code=status.HTTP_200_OK)
async def show_friend_requests(email: Annotated[str, Query(..., description="Email of the user")]):
    response = await FriendsHandler.HandleShowFriendRequests(email)
    return response


@router.delete("/requests/remove", status_code=status.HTTP_200_OK)
async def remove_friend_requests(
    friend_email: Annotated[str, Query(..., description="Email of the friend to remove")],
    user_email: Annotated[str, Query(..., description="Email of the current user")]
):
    response = await FriendsHandler.HandleRemoveFriendRequests(friend_email, user_email)
    return response


@router.delete("/remove", status_code=status.HTTP_200_OK)
async def remove_friend(
    friend_email: Annotated[str, Query(..., description="Email of the friend to remove")],
    user_email: Annotated[str, Query(..., description="Email of the current user")]
):
    response = await FriendsHandler.HandleRemoveFriend(friend_email, user_email)
    return response
