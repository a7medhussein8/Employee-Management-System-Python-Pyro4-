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



