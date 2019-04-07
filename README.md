## Project Description:
This is an implementation of distributed social network based [Django](https://www.djangoproject.com/). This project has a concrete implementation of RESTful API, all of accomplished API can be found [here](https://github.com/sajjadhaiderrr/CMPUT404-Project/wiki/API-Endpoints). By RESTful API, it allows us to connect with other servers, whom are following the same API protocol as we are. Therefore, we can now browse posts made not only by authors on our server, but also authors on other servers that are connecting with us. Servers who are connected with us are determined by the web admin. An authentication credential will be issued if web admin accept to connect with other server.

For remote funcionalities, we will not store any information of posts from other server. But we do temperarily store authors' information for friendship and comments functionalities to work (since it will violates the foreign key constraint if we don't store them). All remote authors' information will be updated if corresponding author interacts with out server.

## Group Member
- Jiahao Guo
- Hussain Khan
- Sajjad Haider
- Yizhou Zhao

## Reference
- Django Rest framework: https://www.django-rest-framework.org/
- django-bootstrap4: https://pypi.org/project/django-bootstrap4/
- showdownjs: http://showdownjs.com/
