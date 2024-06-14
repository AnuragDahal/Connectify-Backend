from ...Auth.authhandler import Validate
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
        is_user = Validate.verify_email(user_email)
        is_friend = Validate.verify_email(friend_email)
        if is_user and is_friend:
            # accept the request
            accept_request = user_collection.update_one(
                {"email": user_email}, {"$addToSet": {"friends": friend_email}})
            # Add the user_email to the friend's friends list
            user_collection.update_one({"email": friend_email},
                                       {"$addToSet": {"friends": user_email}})
            # # check if the request was accepted
            if accept_request.modified_count == 0:
                return ErrorHandler.ALreadyExists("Friend request already accepted")
            # remove the request from the friend's friend_requests
            remove_request = user_collection.update_one(
                {"email": user_email}, {"$pull": {"friend_requests": friend_email}})
            return {"message": "Friend request accepted"}
        return ErrorHandler.NotFound("User or friend not found")

    @staticmethod
    def HandleShowFriends(user_email: str):
        """Show all the friends of the user.
        """
        user_doc = user_collection.find_one({"email": user_email})
        if user_doc:
            if user_doc['friends']:
                return user_doc['friends']
            return ErrorHandler.NotFound("No friends found")
        return ErrorHandler.NotFound("User not found")

    @staticmethod
    def HandleShowFriendRequests(email: str):
        """Show all the friend requests of the user.
        """
        user_doc = user_collection.find_one({"email": email})
        if user_doc:
            if user_doc['friend_requests']:
                return user_doc['friend_requests']
            return ErrorHandler.NotFound("No friend requests found")
        return ErrorHandler.NotFound("User not found")

    @staticmethod
    def HandleRemoveFriendRequests(friend_email: str, user_email: str):
        """Remove the friend_req from the friend_requests list
        """
        is_user = Validate.verify_email(user_email)
        is_friend = Validate.verify_email(friend_email)
        if is_user and is_friend:
            remove_request = user_collection.update_one(
                {"email": user_email}, {"$pull": {"friend_requests": friend_email}})
            if remove_request.modified_count == 0:
                return ErrorHandler.NotFound("Friend request not found")
            return {"message": "Friend request removed"}
        return ErrorHandler.NotFound("User or friend not found")

    @staticmethod
    def HandleRemoveFriend(friend_email: str, user_email: str):
        """Remove the friend from the friends list
        """
        is_user = Validate.verify_email(user_email)
        is_friend = Validate.verify_email(friend_email)
        if is_user and is_friend:
            remove_friend = user_collection.update_one(
                {"email": user_email}, {"$pull": {"friends": friend_email}})
            if remove_friend.modified_count == 0:
                return ErrorHandler.NotFound("Friend not found")
            return {"message": "Friend removed"}
        return ErrorHandler.NotFound("User or friend not found")
