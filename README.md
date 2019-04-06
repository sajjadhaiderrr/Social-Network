# CMPUT404-Project
This is CMPUT404 project. This is a distributed social network. Written by:
- Jiahao Guo
- Hussain Khan
- Sajjad Haider
- Yizhou Zhao
## Project Structure
This project is consisted by three apps:
- Accounts
    - Handling functionalities related with authors. Including:
        - Sign-up
        - Login
        - Search for other users by their display names.
        - Viewing profile of current logined user.
        - Viewing profile of other user's profile on this server.
        - Viewing profile of other user's profile on other authorized server.
        - Be friend with other users. This is done by allowing current user to:
            - Follow other users
                - Send friend request automatically when current user is following other users
            - Get followed back by other users
        - Un-friend with other users. This is done by allowing current user to:
            - Unfollow other users
    - Contains pages:
        - Home page of entire project
            - redirect to current user's home page if user is authenticated.
            - redirect to login page if user is not authenticated.
        - Login page
            - Allow user to login
        - Sign-up page
            - Allow user to create an account as author
        - Home page of current user
            - Allow current user (logined) to browse every posts that are visible to him/her. All posts are sorted by published time, from newest at top to oldest at bottom.
            - Allow current user to add comments on every posts.
            - Allow current user to search for all authors on current server.
            - Logout
            - Having the following entries to:
                - View a list of friends
                - View a list of followers
                - View a list of authors that current user is following
                - View current user's profile and all posts current user made
                - Create post
        - Profile page
            - Allow current user to browse his/her own profile
                - Allow current user to browse every posts he/she made
                - Allow current user to edit his/her profile
            - Allow current user to browse other user's profile
                - Allow current user to browser posts of the author he/she is viewing that are visible to current user
                - Allow current user to follow/unfollow the author he/she is viewing.
        - Friends/Following/Follers list page
            - Populate a list of authors that are either friends/following/followers of given user.
            - The list is based on the query browser send to server.
        - Notification page
            - Display all friend requests that current user didn't respond.
            - Allow current user to respond friend reqeusts, by either:
                - Following back the author who sent this friend request
                - Ignoring the friend request. In this case, friend requests will not be shown any more.       
    - For more information: check this wiki page
- api
    - Handling functionalities related with to RESTful API. Including:
        - Receiving and responding requests from clients (Ajax)
        - Receiving and responding requests from other authorized server.
    - For more information: check this wiki page
- posting
    - Handling functionalities related with posts. Including:
        - Create a post
            - that has a image (png/jpg)
            - that are only visible to me
            - that are visble to a list of friends I choose
            - that are only visible to my friends
            - that are only visible to my friends and friends of friends
            - that are only visible to authors on my server
            - that are public
        - View a single post
            - Allow user to see one of posts that are visible to him/her in a single page
            - Allow user to see comments of that post
            - Allow user to add comment on that post
    - For more information: check this wiki page
        

## Reference
- Django Rest framework: https://www.django-rest-framework.org/
- django-bootstrap4: https://pypi.org/project/django-bootstrap4/
- showdownjs: http://showdownjs.com/
             
            
