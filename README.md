# attendance_app

attendance_app description

## First Requirements

The requirements to run the app it's just have Docker Engine installed

# Development

- Run a terminal on attendance_app/
- In that folder run "docker-compose up"
- This will run 3 services, MySQL (it will be initialized with demo data), Influx DB and the Backend Service
- Each service will run on "localhost"
- :8000 --> Backend
- :8086 --> InfluxDB
- :3306 --> MySQL

- In order to test the application you can make requests to the endpoint using Swagger or with PostMan or other tools like that.
  Endpoint Documentation: http://localhost:8000/docs

- And there are influx demo data to test the POST request in the file attendance_app/db/demo_data.json
