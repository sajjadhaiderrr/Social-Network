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
            
        - Viewing profile of other user's profile.
            
        - Following other users.
        - Unfollowing other users.
    - Also contains pages that showing:
        - Login page
            - `/author/signin/`
        - Sign-up page
            - `/author/signup/`
        - Current user's home page
            - `/author/{author_id}/`
        - Current user's profile
            - `/author/{author_id}/info/`
        - Current user's friends
            - `/author/{author_id}/friends/`
        - Other user's profile
            - `/author/{author_id}/info/`
        - Search result of other users.
            - `/author/searchresult/?search={term}`
- api
    - The following apis are implemented:
        - Authors:
            - `/author/{author_id}`
                - `GET`: Get a author's profile.
            - `/author/{author_id}/friends`
                - `GET`: Get a list of author.
                - `POST`: Ask a service if anyone in the list is a friend.
            - `/author/{author1_id}/friends/{author2_id}`
                - `GET`: Ask if 2 authors are friends.
            - `/friendrequest`
                - `POST`: Make a friend request
            - `/unfriendrequest`
                - `POST`: Make an unfriend request
            - `/author/{author_id}/following`
                - `GET`: Get a list of authors that current author is following.
            - `/author/{author_id}/follower`
                - `GET`: Get a list of authors that are following current author.
- posting
    - The following apis are implemented:
        - Posts:           
            - `/posts/`
                - `GET`: Get all posts marked as public on the server
                - `POST`: Create a new post
            - `/posts/{post_id}`
                - `GET`: Get a post by post id
                - `PUT`: Update a post by post id
                - `DELETE`: Delete a post by post id
                
            - `/posts/{post_id}/comments`
                - `GET`: Get comments of a post
                - `POST`: Add a comment to a post

## Reference
- Django Rest framework: https://www.django-rest-framework.org/
- django-bootstrap4: https://pypi.org/project/django-bootstrap4/
- showdownjs: http://showdownjs.com/
             
            
