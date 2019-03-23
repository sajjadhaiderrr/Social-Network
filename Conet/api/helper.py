from Accounts.models import Author, Friendship 

class ApiHelper:
    def check_friend_of_friend(self):
        
        return True


    def get_all_friend_requests(self, authorObj):
        friendRequests = Friendship.objects.filter(recv_id=authorObj, state=0) # pylint: disable=maybe-no-member
        return friendRequests

    def get_two_authors_relation(self, authorObj1, authorObj2):
        #friendship = Friendship.objects.filter(init_id=authorObj1, recv_id=authorObj2)
        #reverse_friendship = Friendship.objects.filter(init_id=authorObj2, recv_id=authorObj1)
        return None