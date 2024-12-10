# pathao_assignment

# Run commmand

cd PathaoFarmer

docker-compose build --no-cache

docker-compose up

# Run Migrations

docker-compose exec web python manage.py makemigrations

docker-compose exec web python manage.py migrate

# Run tests

docker-compose exec web python manage.py test


# Create Superuser

docker-compose exec web python manage.py createsuperuser


# Test using Postman

Import the postman schema to test the api endpoints using postman