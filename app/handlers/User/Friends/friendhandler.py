from ...Auth.authhandler import Validate
from ....core.database import user_collection
from ...exception import ErrorHandler


class FriendsHandler:

    @staticmethod
    async def _verify_users(*emails):
        """Verify if all provided emails belong to existing users."""
        for email in emails:
            if not await Validate.verify_email(email):
                return False
        return True

    @staticmethod
    async def HandleFriendRequest(email_of_friend: str, email_of_user: str):
        if not await FriendsHandler._verify_users(email_of_friend, email_of_user):
            return ErrorHandler.NotFound("User or friend not found")

        send_request = await user_collection.update_one(
            {"email": email_of_friend}, {"$addToSet": {"friend_requests": email_of_user}})
        sent_req = await user_collection.update_one(
            {"email": email_of_user}, {"$addToSet": {"sent_friend_requests": email_of_friend}})

        if send_request.modified_count and sent_req.modified_count == 0:
            return ErrorHandler.ALreadyExists("Friend request already sent")

        return {"message": "Friend request sent"}

    @staticmethod
    async def HandleFriendAcceptance(friend_email: str, user_email: str):
        if not await FriendsHandler._verify_users(friend_email, user_email):
            return ErrorHandler.NotFound("User or friend not found")

        accept_request = await user_collection.update_one(
            {"email": user_email}, {"$addToSet": {"friends": friend_email}})
        await user_collection.update_one(
            {"email": friend_email}, {"$addToSet": {"friends": user_email}})

        if accept_request.modified_count == 0:
            return ErrorHandler.ALreadyExists("Friend request already accepted")

        await user_collection.update_one(
            {"email": user_email}, {"$pull": {"friend_requests": friend_email}})

        return {"message": "Friend request accepted"}

    @staticmethod
    async def HandleShowFriends(user_logged_in: str):
        user_doc = await user_collection.find_one({"email": user_logged_in})
        if not user_doc:
            return ErrorHandler.NotFound("User not found")

        if user_doc['friends']:
            return user_doc['friends']

        return ErrorHandler.NotFound("No friends found")

    @staticmethod
    async def HandleShowFriendRequests(email: str):
        user_doc = await user_collection.find_one({"email": email})
        if not user_doc:
            return ErrorHandler.NotFound("User not found")

        if user_doc['friend_requests']:
            return user_doc['friend_requests']

        return ErrorHandler.NotFound("No friend requests found")

    @staticmethod
    async def HandleShowSentFriendRequests(user_email: str):
        user_doc = await user_collection.find_one({"email": user_email})
        if not user_doc:
            return ErrorHandler.NotFound("User not found")
        if user_doc['sent_friend_requests']:
            return user_doc['sent_friend_requests']

        return ErrorHandler.NotFound("No sent friend requests found")

    @staticmethod
    async def HandleRemoveFriendRequests(friend_email: str, user_email: str):
        if not await FriendsHandler._verify_users(friend_email, user_email):
            return ErrorHandler.NotFound("User or friend not found")

        # Perform the first update to remove the friend request from the user's sent requests
        remove_received_request = await user_collection.update_one(
            {"email": user_email}, {"$pull": {"friend_requests": friend_email}}
        )

        # Perform the second update to remove the friend request from the friend's received requests
        remove_sent_request = await user_collection.update_one(
            {"email": friend_email}, {"$pull": {"sent_friend_requests": user_email}}
        )

        # Check if either of the updates modified a document
        if remove_sent_request.modified_count == 0 and remove_received_request.modified_count == 0:
            return ErrorHandler.NotFound("Friend request not found")

        return {"message": "Friend request removed"}

    @staticmethod
    async def HandleRemoveFriend(friend_email: str, user_email: str):
        if not await Validate.verify_email(friend_email):
            return ErrorHandler.NotFound("Friend not found")

        remove_friend = await user_collection.update_one(
            {"email": user_email}, {"$pull": {"friends": friend_email}})

        if remove_friend.modified_count == 0:
            return ErrorHandler.NotFound("Friend not found")

        return {"message": "Friend removed"}
