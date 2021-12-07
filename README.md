# Yalantis test task 
To complete the task, a Python3.10 and Django Rest Framework were used to develop the application.
## Structure of the  Application
The application is divided into 2 django apps: drivers and vehicles. Inside each django app 3 modules were developed: 
serilizers, views and services. 

Serilizers - this module validates data and also permofms serialization/deserilization into/from json 

Views - recieves validated parameters from Serilizers module and calls Services module, depending on the recieved parameters.
Additionaly, Views validate query parameters.

Services - this module directly permofms manipulations with Models 
## Tests
The tests check implemenation of the functional requirements. There is also negative scenarion tests.