import random
from faker import Faker
from django.core.management.base import BaseCommand
from audi_manager.models import *


# NUM_PERSONAS = int(5000)  # 5000
# NUM_CLIENTES = int(NUM_PERSONAS * 0.85)  # 4250
# NUM_PAISES = int(30)  # 30
# NUM_POBLACIONES = int(NUM_PAISES * 5)  # 150
# NUM_CONCESIONARIOS = int(NUM_POBLACIONES * 4)  # 600
# NUM_TRABAJADORES = int(NUM_PERSONAS * 0.15)  # 750
# NUM_TECNICOS = int(NUM_TRABAJADORES * 0.6)  # 450
# NUM_COMERCIALES = int(NUM_TRABAJADORES * 0.4)  # 300
# NUM_VALORACIONES = int(NUM_CLIENTES * 1.2)  # 5100
# NUM_VEHICULOS = int(NUM_CONCESIONARIOS * 10)  # 6000
# # 20 motores de cada tipo (gasolina, diesel, hibrido, electrico)
# NUM_MOTORES = int(20 * 4)  # 80
# # todos los vehículos están expuestos
# NUM_EXPOSICIONES = int(NUM_VEHICULOS * 1.5)  # 9000
# NUM_VENTAS = int(NUM_EXPOSICIONES * 0.8)  # 7200

# 🤓☝️


NUM_PERSONAS = int(250000)  # 500000 PERSONAS
NUM_CLIENTES = int(NUM_PERSONAS * 0.85)  # 425000 CLIENTES
NUM_PAISES = int(100)  # 100 PAISES
NUM_POBLACIONES = int(NUM_PAISES * 30)  # 3000 POBLACIONES
NUM_CONCESIONARIOS = int(NUM_POBLACIONES * 4)  # 12000 CONCESIONARIOS
NUM_TRABAJADORES = int(NUM_PERSONAS * 0.15)  # 75000 TRABAJADORES
NUM_TRABAJADORES_CLIENTES = 0.1 * NUM_PERSONAS
NUM_TECNICOS = int(NUM_TRABAJADORES * 0.6)  # 45000 TECNICOS
NUM_COMERCIALES = int(NUM_TRABAJADORES * 0.4)  # 30000 COMERCIALES
NUM_VALORACIONES = int(NUM_CLIENTES * 1.2)  # 510000 VALORACIONES
NUM_VEHICULOS = int(NUM_CONCESIONARIOS * 10)  # 120000 VEHICULOS
NUM_MOTORES = int(20 * 4)  # 80 MOTORES
NUM_EXPOSICIONES = int(NUM_VEHICULOS * 1.5)  # 180000 EXPOSICIONES
NUM_VENTAS = int((NUM_TRABAJADORES_CLIENTES + NUM_CLIENTES) * 1.2)  # 144000 VENTAS


class Command(BaseCommand):
    help = "Create example data"

    def split_list_by_percentage(lst, percentages):
        """
        Splits a list into sublists based on percentages.

        :param lst: the list to split
        :param percentages: a list of percentages to split by
        :return: a list of sublists
        """
        total_size = len(lst)
        sublists = []
        start = 0
        for percentage in percentages:
            size = int(total_size * percentage)
            sublist = []
            while len(sublist) < size:
                sublist.append(lst[start])
                start += 1
            sublists.append(sublist)
        return sublists

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Delete schema

        print("Borrando datos anteriores...")
        # Drop all info from tables

        nombres = []
        for i in range(500):
            nombres.append(fake.unique.name())

        # Persona(DNI, nombre, num_tel)
        # PK DNI
        # UK num_tel
        print(f"Añadiendo {NUM_PERSONAS} personas")
        personas = []
        while len(personas) < NUM_PERSONAS:
            dni = fake.unique.bothify(text="########").upper()
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            letra = tabla[int(dni) % 23]
            dni = dni + letra
            num_tel = fake.unique.bothify(text="6########")
            nombre = random.choice(nombres)
            username = fake.unique.user_name()
            password = fake.password()

            p = Persona(
                dni=dni,
                nombre=nombre,
                num_tel=num_tel,
                username=username,
                password=password,
            )
            personas.append(p)
        Persona.objects.bulk_create(personas)
        print(f"{len(personas)} personas added.")

        # Dividimos personas en clientes y trabajadores y ambos en un 80% y 10% y 10% respectivamente
        (
            personas_clientes,
            personas_trabajadores,
            personas_ambos,
        ) = Command.split_list_by_percentage(personas, [0.80, 0.10, 0.10])

        # Cliente(DNI, email)
        # PK FK DNI a Persona(dni)
        # UK email
        clientes = []
        print(f"Añadiendo {len(personas_clientes)+len(personas_ambos)} clientes")
        for persona in personas_clientes + personas_ambos:
            email = fake.unique.email()
            c = Cliente(
                persona=persona,
                email=email,
                num_tel=persona.num_tel,
                nombre=persona.nombre,
                username=persona.username,
                password=persona.password,
            )
            clientes.append(c)
            c.save()

        print(f"{len(clientes)} clientes added.")

        # Pais(nombre)
        # PK nombre
        paises = []
        print(f"Añadiendo {NUM_PAISES} países")
        while len(paises) < NUM_PAISES:
            nombre = fake.unique.country()
            if len(nombre) < 50:
                p = Pais(nombre=nombre)
                paises.append(p)
        Pais.objects.bulk_create(paises)
        print(f"{len(paises)} países added.")

        # Poblacion(nombre, pais)
        # PK (nombre, pais)
        # FK pais a pais(nombre)
        poblaciones = []
        unique_records = set()
        print(f"Añadiendo {NUM_POBLACIONES} poblaciones")
        while len(poblaciones) < NUM_POBLACIONES:
            nombre = fake.city()
            pais = random.choice(paises)
            if not (nombre, pais) in unique_records:
                unique_records.add((nombre, pais))
                p = Poblacion(nombre=nombre, pais=pais)
                poblaciones.append(p)
        Poblacion.objects.bulk_create(poblaciones)
        print(f"{len(poblaciones)} poblaciones added.")

        # Concesionario(num_tel, email, poblacion)
        # UK email
        # PK num_tel
        # FK poblacion a poblacion(nombre)
        print(f"Añadiendo {NUM_CONCESIONARIOS} concesionarios")
        concesionarios = []
        while len(concesionarios) < NUM_CONCESIONARIOS:
            num_tel = fake.unique.bothify(text="9########")
            email = fake.unique.email()
            poblacion = random.choice(poblaciones)
            c = Concesionario(num_tel=num_tel, email=email, poblacion=poblacion)
            concesionarios.append(c)
        Concesionario.objects.bulk_create(concesionarios)
        print(f"{len(concesionarios)} concesionarios added.")

        # Trabajador(DNI, experiencia, disponibilidad, concesionario)
        # PK FK DNI a Persona(dni)
        # FK concesionario a concesionario(num_tel)
        trabajadores = []
        print(
            f"Añadiendo {len(personas_trabajadores)+len(personas_ambos)} trabajadores"
        )
        for persona in personas_trabajadores + personas_ambos:
            experiencia = random.randint(0, 50)
            disponibilidad = random.choice(["Mañana", "Tarde", "Completa"])
            concesionario = random.choice(concesionarios)
            # print(persona, experiencia, disponibilidad, concesionario)
            t = Trabajador(
                persona=persona,
                experiencia=experiencia,
                disponibilidad=disponibilidad,
                concesionario=concesionario,
                num_tel=persona.num_tel,
                nombre=persona.nombre,
                username=persona.username,
                password=persona.password,
            )
            trabajadores.append(t)
            t.save()
        print(f"{len(trabajadores)} trabajadores added.")

        # Dividir trabajadores en comerciales y tecnicos en un 60/40
        (
            trabajadores_comerciales,
            trabajadores_tecnicos,
        ) = Command.split_list_by_percentage(trabajadores, [0.60, 0.40])

        # Tecnico(DNI, especializacion)
        # PK FK DNI a Trabajador(dni)
        tecnicos = []
        unique_records = set()
        print(f"Añadiendo {len(trabajadores_tecnicos)} técnicos")
        for _trabajador in trabajadores_tecnicos:
            especializacion = random.choice(["Mecanica", "Chapa y pintura"])
            t = Tecnico(
                _trabajador=_trabajador,
                especializacion=especializacion,
                experiencia=_trabajador.experiencia,
                disponibilidad=_trabajador.disponibilidad,
                concesionario=_trabajador.concesionario,
                num_tel=_trabajador.num_tel,
                nombre=_trabajador.nombre,
                username=_trabajador.username,
                password=_trabajador.password,
            )
            tecnicos.append(t)
            t.save()
        print(f"{len(tecnicos)} técnicos added.")

        # Comercial(DNI, email)
        # PK FK DNI a Trabajador(dni)
        # UK email
        comerciales = []
        unique_records = set()
        print(f"Añadiendo {len(trabajadores_comerciales)} comerciales")
        for _trabajador in trabajadores_comerciales:
            email = fake.unique.email()
            c = Comercial(
                _trabajador=_trabajador,
                email=email,
                experiencia=_trabajador.experiencia,
                concesionario=_trabajador.concesionario,
                disponibilidad=_trabajador.disponibilidad,
                num_tel=_trabajador.num_tel,
                nombre=_trabajador.nombre,
                username=_trabajador.username,
                password=_trabajador.password,
            )
            comerciales.append(c)
            c.save()
        print(f"{len(comerciales)} comerciales added.")

        # Valoracion(cliente, concesionario, rating, fecha)
        # FK cliente a cliente(dni)
        # FK concesionario a concesionario(num_tel)
        # PK(cliente, concesionario)
        unique_records = set()
        valoraciones = []
        print(f"Añadiendo {NUM_VALORACIONES} valoraciones")
        while len(unique_records) < NUM_VALORACIONES:
            cliente = random.choice(clientes)
            concesionario = random.choice(concesionarios)
            if not (cliente, concesionario) in unique_records:
                unique_records.add((cliente, concesionario))
                rating = random.randint(0, 5)
                fecha = fake.date_between(start_date="-1y", end_date="today")
                v = Valoracion(
                    cliente=cliente,
                    concesionario=concesionario,
                    rating=rating,
                    fecha=fecha,
                )
                valoraciones.append(v)
        Valoracion.objects.bulk_create(valoraciones)
        print(f"{len(valoraciones)} valoraciones added.")

        # Motor(combustible, potencia)
        # PK (combustible, potencia)
        motores = []
        print(f"Añadiendo {NUM_MOTORES} motores")
        tipos = ["Diesel", "Gasolina", "Hibrido", "Electrico"]
        for i in tipos:
            for j in range(100, 500, 20):
                combustible = i
                potencia = j
                m = Motor(combustible=combustible, potencia=potencia)
                motores.append(m)

        Motor.objects.bulk_create(motores)
        print(f"{len(motores)} motores added.")

        # Vehiculo(num_bastidor, matricula, ano_fabricacion, modelo, descripcion, dni_tecnico)
        # PK num_bastidor
        # FK dni_tecnico a tecnico(dni)
        vehiculos = []
        vehiculos_motores = []
        print(f"Añadiendo {NUM_VEHICULOS} vehiculos")
        diccionario_modelos_motores = {}
        while len(vehiculos) < NUM_VEHICULOS:
            num_bastidor = fake.unique.bothify("????????????????")

            # matricula puede ser null(vehículo nuevo) en un 80% de los casos
            if random.randint(0, 100) < 80:
                matricula = None
            else:
                matricula = fake.unique.bothify("????###")

            ano_fabricacion = fake.year()
            modelo = random.choice(
                [
                    "A1",
                    "A3",
                    "A4",
                    "A4 Allroad Quattro",
                    "A5",
                    "A6 Allroad Quattro",
                    "A6",
                    "A7",
                    "A8",
                    "AAAUGH",
                    "Q2",
                    "Q3",
                    "Q5",
                    "Q7",
                    "R8",
                    "RS Q3",
                    "RS3",
                    "RS4",
                    "RS5",
                    "RS6",
                    "RS7",
                    "S1",
                    "S3",
                    "S4",
                    "S4",
                    "S5",
                    "S6",
                    "S6",
                    "S7",
                    "S7",
                    "S8",
                    "SQ5",
                    "SQ7",
                    "SQ7",
                    "TT",
                    "TTS",
                    "TTS",
                    # Modelos +
                    "A1+",
                    "A3+",
                    "A4+",
                    "A4 Allroad Quattro+",
                    "A5+",
                    "A6 Allroad Quattro+",
                    "A6+",
                    "A7+",
                    "A8+",
                    "AAAUGH+",
                    "Q2+",
                    "Q3+",
                    "Q5+",
                    "Q7+",
                    "R8+",
                    "RS Q3+",
                    "RS3+",
                    "RS4+",
                    "RS5+",
                    "RS6+",
                    "RS7+",
                    "S1+",
                    "S3+",
                    "S4+",
                    "S4+",
                    "S5+",
                    "S6+",
                    "S6+",
                    "S7+",
                    "S7+",
                    "S8+",
                    "SQ5+",
                    "SQ7+",
                    "SQ7+",
                    "TT+",
                    "TTS+",
                    # Modelos ++
                    "A1++",
                    "A3++",
                    "A4++",
                    "A4 Allroad Quattro++",
                    "A5++",
                    "A6 Allroad Quattro++",
                    "A6++",
                    "A7++",
                    "A8++",
                    "AAAUGH++",
                    "Q2++",
                    "Q3++",
                    "Q5++",
                    "Q7++",
                    "R8++",
                    "RS Q3++",
                    "RS3++",
                    "RS4++",
                    "RS5++",
                    "RS6++",
                    "RS7++",
                    "S1++",
                    "S3++",
                    "S4++",
                    "S4++",
                    "S5++",
                    "S6++",
                    "S6++",
                    "S7++",
                    "S7++",
                    "S8++",
                    "SQ5++",
                    "SQ7++",
                    "SQ7++",
                    "TT++",
                    "TTS++",
                    "TTS++",
                ]
            )
            descripcion = fake.text()
            # 20% de no tener tecnico
            tecnico = None
            if not random.randint(0, 20) == 0:
                tecnico = random.choice(tecnicos)

            # print(num_bastidor, matricula, ano_fabricacion,modelo, descripcion, dni_tecnico)
            v = Vehiculo(
                num_bastidor=num_bastidor,
                matricula=matricula,
                ano_fabricacion=ano_fabricacion,
                modelo=modelo,
                descripcion=descripcion,
                tecnico=tecnico,
            )

            vehiculos.append(v)

            # Cada modelo tiene un tipo de motor fijo
            if modelo in diccionario_modelos_motores:
                # El modelo ya existe en el diccionario, asignar motor existente
                motor = diccionario_modelos_motores[modelo]
            else:
                # El modelo no existe en el diccionario, seleccionar un motor aleatorio
                motor = random.choice(motores)
                diccionario_modelos_motores[modelo] = motor

            # Añadimos relacion muchos a muchos
            vehiculos_motores.append(Vehiculo.Motor.through(vehiculo=v, motor=motor))

        Vehiculo.objects.bulk_create(vehiculos)
        Vehiculo.Motor.through.objects.bulk_create(vehiculos_motores)
        print(f"{len(vehiculos)} vehiculos added.")

        # Exposicion(numero, precio, concesionario, vehiculo, km)
        # PK (concesionario, numero)
        # FK concesionario a concesionario(num_tel)
        # FK vehiculo a vehiculo(num_bastidor)
        exposiciones = []
        print(f"Añadiendo {NUM_EXPOSICIONES} exposiciones")
        unique_records = set()
        while len(exposiciones) < NUM_EXPOSICIONES:
            precio = random.randint(100000, 9999999) / 100
            concesionario = random.choice(concesionarios)
            vehiculo = random.choice(vehiculos)
            numero = fake.unique.bothify("######")

            # El 85% de los vehiculos son de km 0
            if random.random() < 0.85:
                km = 0
            else:
                km = random.randint(1, 999999)
            if not (concesionario, vehiculo) in unique_records:
                unique_records.add((concesionario, vehiculo))
                e = Exposicion(
                    numero=numero,
                    precio=precio,
                    concesionario=concesionario,
                    vehiculo=vehiculo,
                    km=km,
                )
                exposiciones.append(e)
        Exposicion.objects.bulk_create(exposiciones)
        print(f"{len(exposiciones)} exposiciones added.")

        # Venta(fecha, precio_final, vehiculo, cliente, dni_comercial, numero_exposicion)
        # PK(cliente, num_bastidor)
        # FK cliente a cliente(dni)
        # FK vehiculo a vehiculo(num_bastidor)
        # FK dni_comercial a comercial(dni)
        # FK numero_exposicion a exposicion(numero) (NOT NULL)
        print(f"Añadiendo {NUM_VENTAS} ventas")
        ventas = []
        unique_records = set()
        i = 0
        while len(ventas) < NUM_VENTAS:
            fecha = fake.date_between(start_date="-1y", end_date="today")
            precio_final = random.randint(100000, 9999999) / 100
            vehiculo = random.choice(vehiculos)
            cliente = clientes[i % len(clientes)]
            comercial = random.choice(comerciales)
            exposicion = random.choice(exposiciones)
            # Mirar que no se pueda vender para el mismo vehiculo
            if not (cliente, vehiculo) in unique_records:
                unique_records.add((cliente, vehiculo))
                v = Venta(
                    fecha=fecha,
                    precio_final=precio_final,
                    vehiculo=vehiculo,
                    cliente=cliente,
                    comercial=comercial,
                    exposicion=exposicion,
                )
                ventas.append(v)
            i += 1

        Venta.objects.bulk_create(ventas)
        print(f"{len(ventas)} ventas added.")
