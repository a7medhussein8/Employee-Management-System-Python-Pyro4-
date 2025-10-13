Run Project Locally (Without Docker).
1-Make sure you have these installed:
- Python 3.11+
- Node.js 18+ and npm
- MongoDB

2- Then install dependencies:
    pip install -r requirements.txt

3- start the MongoDB Server:
    mongod
	
4- Start the Pyro Name Server:
    python -m Pyro4.naming

you should see:
	Pyro Name Server started on 0.0.0.0:9090

5- Start Each Microservice:
- Database Service:
  
	cd database_service

	python database_service.py

- employee Service:
  
	cd employee_service

	python employee_service.py

- notification Service:
  
	cd notification_service

	python notification_service.py

- payroll Service:
  
	cd payroll_service

	python payroll_service.py

- attendance Service:
  
	cd attendance_Service

	python attendance_Service.py

- department Service:
  
	cd department_Service

	python department_Service.py

- Flask Gateway:

  	cd gateway_http
  
	python flask_gateway.py

6- Start the frontend (React App):

	cd frontend
	
	npm install
	
	npm start

7-Then Visit your App: http://localhost:3000.


8-  Verify That All Service Are Conneced: 

   Check the console for these messages 

	[DatabaseService] Ready and registered with NameServer
	[EmployeeService] Ready and registered with NameServer
	[NotificationService] Ready and registered with NameServer
	[FlaskGateway] Running on http://127.0.0.1:5000
	React App running on http://localhost:3000







