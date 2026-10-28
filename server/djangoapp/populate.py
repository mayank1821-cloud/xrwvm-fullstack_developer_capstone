from .models import CarMake, CarModel

def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Set the standard in luxury and performance"},
        {"name": "Audi", "description": "Vorsprung durch Technik"},
        {"name": "Kia", "description": "Movement that inspires"},
        {"name": "Toyota", "description": "Reliable and quality vehicles worldwide"},
    ]

    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(CarMake.objects.create(name=data['name'], description=data['description']))

    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "car_make": car_make_instances[0]},
        {"name": "Qashqai", "type": "SUV", "year": 2023, "car_make": car_make_instances[0]},
        {"name": "X-Trail", "type": "SUV", "year": 2023, "car_make": car_make_instances[0]},
        {"name": "A-Class", "type": "SUV", "year": 2021, "car_make": car_make_instances[1]},
        {"name": "C-Class", "type": "SEDAN", "year": 2022, "car_make": car_make_instances[1]},
        {"name": "E-Class", "type": "SEDAN", "year": 2023, "car_make": car_make_instances[1]},
        {"name": "A4", "type": "SEDAN", "year": 2020, "car_make": car_make_instances[2]},
        {"name": "A5", "type": "SEDAN", "year": 2021, "car_make": car_make_instances[2]},
        {"name": "A6", "type": "SEDAN", "year": 2022, "car_make": car_make_instances[2]},
        {"name": "Sorrento", "type": "SUV", "year": 2020, "car_make": car_make_instances[3]},
        {"name": "Carnival", "type": "SUV", "year": 2021, "car_make": car_make_instances[3]},
        {"name": "Cerato", "type": "SEDAN", "year": 2022, "car_make": car_make_instances[3]},
        {"name": "Corolla", "type": "SEDAN", "year": 2022, "car_make": car_make_instances[4]},
        {"name": "Camry", "type": "SEDAN", "year": 2023, "car_make": car_make_instances[4]},
        {"name": "RAV4", "type": "SUV", "year": 2023, "car_make": car_make_instances[4]},
    ]

    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'],
            car_make=data['car_make'],
            type=data['type'],
            year=data['year']
        )
