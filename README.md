# Yalantis test task 
To complete the task, a Python3.10 and Django Rest Framework were used to develop the application.
## Structure of the  Application
The application is divided into 2 django apps: drivers and vehicles. Inside each django app 3 modules were developed: 
Serializers, views and services. 

Serializers - this module validates data and also performs serialization/deserialization into/from json 

Views - receives validated parameters from serializers module and calls Services module, depending on the received parameters.
Additionally, Views validate query parameters.

Services - this module directly performs manipulations with Models 
## Tests
Tests check implementation of the functional requirements. There is also negative scenario tests.