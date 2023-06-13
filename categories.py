from new_enum import NewEnum


class Home(NewEnum):
    Rent = "Alquiler"
    Light = "Luz"
    Gas = "Gas"
    Water = "Agua"
    Grocery = "Supermercado"
    Phone = "Telefono"
    Internet = "Internet"
    Fixes = "Arreglos"


class Hobby(NewEnum):
    Tortuga = "Tortuga"
    Rehersal = "Ensayo"
    Instrument = "Equipo"


class Ocio(NewEnum):
    Dinner = "Cena"
    Lunch = "Comida"
    Party = "Fiesta"
    Drink = "Cervezas"
    Concert = "Conciertos"
    Experience = "Experiencias"
    Cine = "Cine"
    Museum = "Museo"
    Scape_room = "Escaperoom"


class Salud(NewEnum):
    Psychologist = "Psicologo"
    Dentist = "Dentista"
    Phisyo = "Fisioterapia"
    Gym = "Gimnasio"
    Sport = "Deporte"


class Vacaciones(NewEnum):
    Holiday = "Vacaciones"
    Bridge = "Escapadas"


class Otros(NewEnum):
    Gift = "Regalo"
    Clothing = "Ropa"
    Otros = "Otras compras"


class Categories(NewEnum):
    Home = Home
    Hobby = Hobby
    Ocio = Ocio
    Salud = Salud
    Vacaciones = Vacaciones
    Otros = Otros

    @classmethod
    def categorize(cls, tags):
        for category in cls.get_classes():
            for activity in category.get_values():
                if activity in tags:
                    return category.__name__
