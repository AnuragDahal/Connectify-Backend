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
