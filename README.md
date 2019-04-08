## Project Description:
This is an implementation of a distributed social network based on [Django](https://www.djangoproject.com/). This project has a concrete implementation of a RESTful API, all of the accomplished API can be found [here](https://github.com/sajjadhaiderrr/CMPUT404-Project/wiki/API-Endpoints). By being a RESTful API, we can connect with other servers, whom are following the same API protocol as we are. Therefore, we can browse posts made not only by authors on our server, but also authors on other servers that are connecting with us. Servers who are connected with us are determined by the web admin. An authentication credential will be issued if the web admin accepts an incomming connection with the other server.

For remote funcionalities, we will not store any information of posts hosted on other servers. We do temperarily store authors' information for our friendship and commentting functionalities (as the foreign key constraint will be violated if not stored). All remote authors' information will be updated if corresponding author interacts with our server.

For more information, please visit our [wiki page](https://github.com/sajjadhaiderrr/CMPUT404-Project/wiki)

To view a demo of our project, check out our [Video Demo!](https://youtu.be/oUkNwVjryOQ)

## Project Information
#### Main deployment of our project:

* [http://conet-socialdistribution.herokuapp.com/](http://conet-socialdistribution.herokuapp.com/)
* Admin Account (Do not use admin as a common author):
    * username: andrew
    * password: 123
* Common Author Account:
    * username: Dorrryu
    * password: !@#$%^&*
* Account to connect with [https://myblog-cool.herokuapp.com/](https://myblog-cool.herokuapp.com/)
    * username: conecRemote
    * password: conetRemote
* Account to connect with [http://socialdist2.herokuapp.com/author/login/](http://socialdist2.herokuapp.com/author/login/)
    * username: remote1 
    * password: 123
* Account to connect with us (as [https://myblog-cool.herokuapp.com/](https://myblog-cool.herokuapp.com/)):
    * Do not use this account as a common author
    * username: remotenode2
    * password: remotenode2
* Account to connect with us (as [http://socialdist2.herokuapp.com/author/login/](http://socialdist2.herokuapp.com/author/login/)):
    * Do not use this account as a common author
    * username: remotenode1
    * password: remotenode1


#### Servers connecting with us:

Deleting [`Node`](https://github.com/sajjadhaiderrr/CMPUT404-Project/wiki/Models#node) objects would cause forever-pending issue. To correctly remove `Node` object, you will also need to remove remote [`Author`](https://github.com/sajjadhaiderrr/CMPUT404-Project/wiki/Models#author) objects for corresponding host.

* [http://socialdist2.herokuapp.com/author/login/](http://socialdist2.herokuapp.com/author/login/)
    * This is a duplicate deployment of our project. Technically, we can treat it as a remote host, since every communication are through RESTful API.
    * Common Author Account:
        * username: test1
        * password: apple1996
        
* [https://myblog-cool.herokuapp.com/](https://myblog-cool.herokuapp.com/)

## Group Members
- Jiahao Guo
- Hussain Khan
- Sajjad Haider
- Yizhou Zhao

## Reference
- Django Rest framework: https://www.django-rest-framework.org/
- django-bootstrap4: https://pypi.org/project/django-bootstrap4/
- showdownjs: http://showdownjs.com/
- django-cors-headers: https://github.com/ottoyiu/django-cors-headers
