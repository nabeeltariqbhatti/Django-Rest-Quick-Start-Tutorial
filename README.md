# Django-Rest-Quick-Start-Tutorial


[Documentation Link](https://www.django-rest-framework.org/tutorial/quickstart/)

Quickstart
We're going to create a simple API to allow admin users to view and edit the users and groups in the system.

Project setup
Create a new Django project named tutorial, then start a new app called quickstart.

# Create the project directory
mkdir tutorial
cd tutorial

# Create a virtual environment to isolate our package dependencies locally
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install Django and Django REST framework into the virtual environment
pip install django
pip install djangorestframework

# Set up a new project with a single application
django-admin startproject tutorial .  # Note the trailing '.' character
cd tutorial
django-admin startapp quickstart
cd ..
The project layout should look like:

$ pwd<br/>
<some path>/tutorial<br/>
$ find .<br/>
.
./manage.py<br/>
./tutorial<br/>
./tutorial/__init__.py<br/>
./tutorial/quickstart<br/>
./tutorial/quickstart/__init__.py<br/>
./tutorial/quickstart/admin.py<br/>
./tutorial/quickstart/apps.py<br/>
./tutorial/quickstart/migrations<br/>
./tutorial/quickstart/migrations/__init__.py<br/>
./tutorial/quickstart/models.py<br/>
./tutorial/quickstart/tests.py<br/>
./tutorial/quickstart/views.py<br/>
./tutorial/settings.py<br/>
./tutorial/urls.py<br/>
./tutorial/wsgi.py<br/>
It may look unusual that the application has been created within the project directory. Using the project's namespace avoids name clashes with external modules (a topic that goes outside the scope of the quickstart).<br/>

Now sync your database for the first time:<br/>

python manage.py migrate<br/>
We'll also create an initial user named admin with a password of password123. We'll authenticate as that user later in our example.<br/>

python manage.py createsuperuser --email admin@example.com --username admin <br/>
Once you've set up a database and the initial user is created and ready to go, open up the app's directory and we'll get coding...<br/>

Serializers
First up we're going to define some serializers. Let's create a new module named tutorial/quickstart/serializers.py that we'll use for our data representations.<br/>

from django.contrib.auth.models import User, Group<br/>
from rest_framework import serializers<br/>


class UserSerializer(serializers.HyperlinkedModelSerializer):<br/>
    class Meta:<br/>
        model = User<br/>
        fields = ['url', 'username', 'email', 'groups']<br/>


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
Notice that we're using hyperlinked relations in this case with HyperlinkedModelSerializer. You can also use primary key and various other relationships, but hyperlinking is good RESTful design.

Views
Right, we'd better write some views then. Open tutorial/quickstart/views.py and get typing.

from django.contrib.auth.models import User, Group<br/>
from rest_framework import viewsets<br/>
from rest_framework import permissions<br/>
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer<br/>


class UserViewSet(viewsets.ModelViewSet):<br/>
    """
    API endpoint that allows users to be viewed or edited.
    """<br/>
    queryset = User.objects.all().order_by('-date_joined')<br/>
    serializer_class = UserSerializer<br/>
    permission_classes = [permissions.IsAuthenticated]<br/>


class GroupViewSet(viewsets.ModelViewSet):<br/>
    """
    API endpoint that allows groups to be viewed or edited.
    """<br/>
    queryset = Group.objects.all()<br/>
    serializer_class = GroupSerializer<br/>
    permission_classes = [permissions.IsAuthenticated]<br/>
Rather than write multiple views we're grouping together all the common behavior into classes called ViewSets.<br/>

We can easily break these down into individual views if we need to, but using viewsets keeps the view logic nicely organized as well as being very concise.<br/>

URLs<br/>
Okay, now let's wire up the API URLs. On to tutorial/urls.py...<br/>

from django.urls import include, path<br/>
from rest_framework import routers<br/>
from tutorial.quickstart import views<br/>

router = routers.DefaultRouter()<br/>
router.register(r'users', views.UserViewSet)<br/>
router.register(r'groups', views.GroupViewSet)<br/>

# Wire up our API using automatic URL routing.<br/>
# Additionally, we include login URLs for the browsable API.<br/>
urlpatterns = [<br/>
    path('', include(router.urls)),<br/>
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))<br/>
]<br/>
Because we're using viewsets instead of views, we can automatically generate the URL conf for our API, by simply registering the viewsets with a router class.<br/>

Again, if we need more control over the API URLs we can simply drop down to using regular class-based views, and writing the URL conf explicitly.<br/>

Finally, we're including default login and logout views for use with the browsable API. That's optional, but useful if your API requires authentication and you want to use the browsable API.

Pagination
Pagination allows you to control how many objects per page are returned. To enable it add the following lines to tutorial/settings.py

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
Settings
Add 'rest_framework' to INSTALLED_APPS. The settings module will be in tutorial/settings.py

INSTALLED_APPS = [
    ...
    'rest_framework',
]
Okay, we're done.

Testing our API
We're now ready to test the API we've built. Let's fire up the server from the command line.

python manage.py runserver<br/>
We can now access our API, both from the command-line, using tools like curl...

bash: curl -H 'Accept: application/json; indent=4' -u admin:password123 http://127.0.0.1:8000/users/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "admin@example.com",
            "groups": [],
            "url": "http://127.0.0.1:8000/users/1/",
            "username": "admin"
        },
        {
            "email": "tom@example.com",
            "groups": [],
            "url": "http://127.0.0.1:8000/users/2/",
            "username": "tom"
        }
    ]
}
Or using the httpie, command line tool...<br/>

bash: http -a admin:password123 http://127.0.0.1:8000/users/

HTTP/1.1 200 OK
...
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "admin@example.com",
            "groups": [],
            "url": "http://localhost:8000/users/1/",
            "username": "paul"
        },
        {
            "email": "tom@example.com",
            "groups": [],
            "url": "http://127.0.0.1:8000/users/2/",
            "username": "tom"
        }
    ]
}




![](https://www.django-rest-framework.org/img/quickstart.png)




[Documentation Link](https://www.django-rest-framework.org/tutorial/1-serialization/)



Tutorial 1: Serialization



Introduction<br/>
This tutorial will cover creating a simple pastebin code highlighting Web API. Along the way it will introduce the various components that make up REST framework, and give you a comprehensive understanding of how everything fits together.
<br/>
The tutorial is fairly in-depth, so you should probably get a cookie and a cup of your favorite brew before getting started. If you just want a quick overview, you should head over to the quickstart documentation instead.
