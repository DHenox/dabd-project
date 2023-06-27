from django.db import models

# Create your models here.

# Persona(DNI, nombre, num_tel)
# PK DNI
# UK num_tel


class Persona(models.Model):
    dni = models.CharField(max_length=9, primary_key=True)
    nombre = models.CharField(max_length=50, blank=False)
    num_tel = models.CharField(max_length=9, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return f"[ DNI: {self.dni} , NOMBRE: {self.nombre} , TEL: {self.num_tel} ]"


# Cliente(DNI, email)
# PK FK DNI a Persona(dni)
# UK email
class Cliente(Persona):
    persona = models.OneToOneField(
        Persona,
        db_column="dni",
        primary_key=True,
        parent_link=True,
        on_delete=models.CASCADE,
    )
    email = models.EmailField(unique=True)

    # Asociativos
    Venta = models.ManyToManyField("Vehiculo", through="Venta")
    Valoracion = models.ManyToManyField("Concesionario", through="Valoracion")

    def __str__(self):
        return f"[ DNI: {self.dni} , NOMBRE: {self.nombre} , EMAIL: {self.email} ]"


# Pais(nombre)
# PK nombre
class Pais(models.Model):
    nombre = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return f"[ PAIS: {self.nombre} ]"


# Poblacion(nombre, nombre_pais)
# PK (nombre, nombre_pais)
# FK nombre_pais a pais(nombre)
class Poblacion(models.Model):
    nombre = models.CharField(max_length=50)
    pais = models.ForeignKey(Pais, db_column="pais", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("nombre", "pais")

    def __str__(self):
        return f"[NOMBRE: {self.nombre} , PAIS: {self.pais.nombre}]"


# Concesionario(num_tel, email, poblacion)
# PK num_tel
# UK email
# FK poblacion a poblacion(nombre)
class Concesionario(models.Model):
    num_tel = models.CharField(max_length=9, primary_key=True)
    email = models.EmailField(unique=True)
    poblacion = models.ForeignKey(
        Poblacion, db_column="poblacion", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"[ TEL: {self.num_tel} , POBLACION: {self.poblacion}]"


# Trabajador(DNI, experiencia, disponibilidad, concesionario)
# PK FK DNI a Persona(dni)
# FK concesionario a concesionario(num_tel)
class Trabajador(Persona):
    persona = models.OneToOneField(
        Persona,
        db_column="dni",
        primary_key=True,
        parent_link=True,
        on_delete=models.CASCADE,
    )
    experiencia = models.IntegerField()
    disponibilidad = models.CharField(max_length=50)
    concesionario = models.ForeignKey(
        Concesionario, db_column="num_tel", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"[ DNI: {self.dni} , NOMBRE: {self.nombre} , CONCESIONARIO: {self.concesionario} ]"


# Tecnico(DNI, especializacion)
# PK FK DNI a Trabajador(dni)
class Tecnico(Trabajador):
    _trabajador = models.OneToOneField(
        Trabajador,
        db_column="dni",
        primary_key=True,
        parent_link=True,
        on_delete=models.CASCADE,
    )
    especializacion = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.dni}, {self.especializacion}"


# Comercial(DNI, email)
# PK FK DNI a Trabajador(dni)
# UK email
class Comercial(Trabajador):
    _trabajador = models.OneToOneField(
        Trabajador,
        db_column="dni",
        primary_key=True,
        parent_link=True,
        on_delete=models.CASCADE,
    )
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.dni}, {self.email}"


# Valoracion(cliente, concesionario, rating, fecha)
# FK cliente a cliente(dni)
# FK concesionario a concesionario(num_tel)
# PK(cliente, concesionario)
class Valoracion(models.Model):
    cliente = models.ForeignKey(
        Cliente, db_column="dni_cliente", on_delete=models.CASCADE
    )
    concesionario = models.ForeignKey(
        Concesionario, db_column="num_tel_concesionario", on_delete=models.CASCADE
    )
    rating = models.IntegerField()
    fecha = models.DateField()

    class Meta:
        unique_together = ("cliente", "concesionario")

    def __str__(self):
        return f"[ DNI: {self.cliente.dni}, NUM_TEL_CONCESIONARIO: {self.concesionario.num_tel}, RATING: {self.rating}, FECHA: {self.fecha} ]"


# Vehiculo(num_bastidor, matricula, ano_fabricacion, modelo, descripcion, tecnico)
# PK num_bastidor
# FK tecnico a tecnico(dni)
class Vehiculo(models.Model):
    num_bastidor = models.CharField(max_length=17, primary_key=True)
    matricula = models.CharField(max_length=7, null=True, blank=True)
    ano_fabricacion = models.IntegerField()
    modelo = models.CharField(max_length=50)
    descripcion = models.TextField()

    # No todos los vehiculos tienen un tecnico asignado actualmente
    tecnico = models.ForeignKey(
        Tecnico,
        db_column="dni_tecnico",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    # Vehiculo-motor
    Motor = models.ManyToManyField("Motor")

    def __str__(self):
        return f"[{self.num_bastidor} {self.modelo}]"


# Motor(combustible, potencia)
# PK (combustible, potencia)
class Motor(models.Model):
    combustible = models.CharField(max_length=50)
    potencia = models.IntegerField()

    class Meta:
        unique_together = ("combustible", "potencia")

    def __str__(self):
        return f"[{self.combustible} {self.potencia}]"


# Exposicion(concesionario, numero, precio, km, vehiculo)
# FK concesionario a concesionario(num_tel)
# FK vehiculo a vehiculo(num_bastidor)
# PK (concesionario, numero)
class Exposicion(models.Model):
    concesionario = models.ForeignKey(
        Concesionario, db_column="num_tel_concesionario", on_delete=models.CASCADE
    )
    numero = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    km = models.IntegerField()
    vehiculo = models.ForeignKey(
        Vehiculo, db_column="num_bastidor_vehiculo", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("concesionario", "numero")

    def __str__(self):
        return f"[ {self.concesionario.num_tel}, {self.numero}, {self.vehiculo.num_bastidor}, {self.km} ]"


# Venta(fecha, precio_final, vehiculo, cliente, comercial, exposicion)
# FK cliente a cliente(dni)
# FK vehiculo a vehiculo(num_bastidor)
# FK comercial a comercial(dni)
# FK exposicion a exposicion(numero) (NOT NULL)
# PK(cliente, num_bastidor)
class Venta(models.Model):
    fecha = models.DateField()

    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    vehiculo = models.ForeignKey(
        Vehiculo, db_column="num_bastidor_vehiculo", on_delete=models.CASCADE
    )
    cliente = models.ForeignKey(
        Cliente, db_column="dni_cliente", on_delete=models.CASCADE
    )
    comercial = models.ForeignKey(
        Comercial, db_column="dni_comercial", on_delete=models.CASCADE
    )

    # Asociativo
    exposicion = models.ForeignKey(Exposicion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("cliente", "vehiculo")

    def __str__(self):
        return f"[ CLIENTE: {self.cliente}, VEHICULO: {self.vehiculo} ]"


# Vehiculo_motor(vehiculo, combustible_motor, potencia_motor)
# PK(vehiculo, combustible_motor, potencia_motor)
# FK combustible_motor a motor(combustible)
# FK potencia_motor a motor(potencia)
# FK vehiculo a vehiculo(num_bastidor)
