from typing import Optional
from ....core.database import user_collection
from ...exception import ErrorHandler


class FriendsHandler:

    @staticmethod
    def HandleFriendRequest(email_of_friend: str, email_of_user: str):
        """Send a friend request to the user.
        """
        is_user = user_collection.find_one({"email": email_of_friend})
        is_friend = user_collection.find_one({"email": email_of_user})
        if is_user and is_friend:
            # send the request to the user
            send_request = user_collection.update_one(
                {"email": email_of_friend}, {"$addToSet": {"friend_requests": email_of_user}})
            # check if the request was sent
            if send_request.modified_count == 0:
                return ErrorHandler.ALreadyExists("Friend request already sent")
            return {"message": "Friend request sent"}
        return ErrorHandler.NotFound("User or friend not found")

    @staticmethod
    def HandleFriendAcceptance(friend_email: str, user_email: str):
        """Accept the friend request from the user.
        """
        is_user = user_collection.find_one({"email": user_email})
        is_friend = user_collection.find_one({"email": friend_email})
        if is_user and is_friend:
            # accept the request
            accept_request = user_collection.update_one(
                {"email": user_email}, {"$addToSet": {"friends": friend_email}})
            # # check if the request was accepted
            if accept_request.modified_count == 0:
                return ErrorHandler.ALreadyExists("Friend request already accepted")
            # remove the request from the friend's friend_requests
            remove_request = user_collection.update_one(
                {"email": user_email}, {"$pull": {"friend_requests": friend_email}})
            return {"message": "Friend request accepted"}
        return ErrorHandler.NotFound("User or friend not found")

    @staticmethod
    def HandleShowFriends(email: str):
        """Show all the friends of the user.
        """
        user = user_collection.find_one({"email": email})
        if user:
            if user["friends"]:
                return user["friends"]
            return ErrorHandler.NotFound("No friends found")
        return ErrorHandler.NotFound("User not found")

    @staticmethod
    def HandleShowFriendRequests(email: str):
        """Show all the friend requests of the user.
        """
        user = user_collection.find_one({"email": email})
        if user:
            if user["friend_requests"]:
                return user["friend_requests"]
            return ErrorHandler.NotFound("No friend requests found")
