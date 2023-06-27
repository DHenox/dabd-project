from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.db.models import Avg, Count
from django.db.models.functions import Round
from django import template
import sys

register = template.Library()


@register.filter
def div_five(value):
    return value / 5


# MENU
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Hard-coded username and password
        if username == "trabajador" and password == "trabajador":
            print("admin")
            # dni de un trabajdor random xd
            dni = Trabajador.objects.order_by("?").first().dni
            request.session["user_id"] = dni
            request.session["is_trabajador"] = True
            return redirect("dashboard")
        elif username == "cliente" and password == "cliente":
            print("cliente")
            # dni de un cliente random xd
            # get random dni from db  from clientes
            dni = Cliente.objects.order_by("?").first().dni
            request.session["user_id"] = dni
            request.session["is_trabajador"] = False
            return redirect("dashboard")
        # Check if the user exists in the database
        try:
            user = Persona.objects.get(username=username, password=password)
        except Persona.DoesNotExist:
            user = None

        if user is not None:
            # Store user information in the session
            request.session["user_id"] = user.dni

            # check if user is cliente or trabajador
            try:
                trabajador = Trabajador.objects.get(
                    username=username, password=password
                )
            except Trabajador.DoesNotExist:
                trabajador = None

            # Parametro para saber si es trabajador o no
            request.session["is_trabajador"] = trabajador is not None
            # Redirect to the dashboard page after successful login
            return redirect("dashboard")
        else:
            # Display an error message if login fails
            error_message = "Invalid username or password."
            return render(request, "login/login.html", {"error_message": error_message})

    return render(request, "login/login.html")


def logout(request):
    # Delete user information from the session
    try:
        del request.session["user_id"]
        del request.session["is_trabajador"]
    except KeyError:
        pass
    # Redirect to the login page after logout
    return redirect("login")


def dashboard(request):
    # Retrieve user information from the session
    user_id = request.session.get("user_id")

    # Retrieve the user from the database based on the stored user_id
    try:
        user = Persona.objects.get(dni=user_id)
    except Persona.DoesNotExist:
        user = None

    if user is not None:
        return render(
            request,
            "dashboard.html",
            {"user": user, "is_trabajador": request.session.get("is_trabajador")},
        )
    else:
        # Redirect to the login page if user information is not found in the session
        return redirect("login")


# LISTS
def list_personas(request):
    name_query = request.GET.get("name", "")
    dni_query = request.GET.get("dni", "")

    personas_list = Persona.objects.all()

    if name_query != "":
        personas_list = personas_list.filter(Q(nombre__istartswith=name_query))
    if dni_query != "":
        personas_list = personas_list.filter(dni__istartswith=dni_query)

    # Set the number of items per page
    paginator = Paginator(personas_list, 8)

    page_number = request.GET.get("page")
    personas_page = paginator.get_page(page_number)

    context = {
        "personas_page": personas_page,
        "name_query": name_query,
        "personas_count": personas_list.count(),
        "dni_query": dni_query,
    }
    return render(request, "persona/list_personas.html", context)


def list_clientes(request):
    name_query = request.GET.get("name", "")
    dni_query = request.GET.get("dni", "")
    print(name_query, dni_query)
    clientes_list = Cliente.objects.all()
    concesionarios_list = Concesionario.objects.all()

    if name_query != "":
        clientes_list = clientes_list.filter(Q(persona__nombre__istartswith=name_query))

    if dni_query != "":
        clientes_list = clientes_list.filter(persona__dni__istartswith=dni_query)

    # Set the number of items per page
    paginator = Paginator(clientes_list, 8)

    page_number = request.GET.get("page")
    clientes_page = paginator.get_page(page_number)

    context = {
        "clientes_page": clientes_page,
        "clientes_count": clientes_list.count(),
        "name_query": name_query,
        "dni_query": dni_query,
        "concesionarios_list": concesionarios_list,
    }
    return render(request, "cliente/list_clientes.html", context)


def list_paises(request):
    nombre_query = request.GET.get("nombre", "")

    paises_list = Pais.objects.all()
    if nombre_query != "":
        paises_list = paises_list.filter(nombre__istartswith=nombre_query)

    paginator = Paginator(paises_list, 10)
    page_number = request.GET.get("page")
    paises_page = paginator.get_page(page_number)

    num_ventas = []

    # QUERY PARA SACAR NUMERO DE VENTAS POR PAÍS
    # SELECT pa.nombre, COUNT(*) AS cantidad_ventas
    # FROM audi_manager_venta AS v
    # INNER JOIN audi_manager_exposicion AS e ON v.exposicion_id = e.id
    # INNER JOIN audi_manager_concesionario AS c ON e.num_tel_concesionario = c.num_tel
    # INNER JOIN audi_manager_poblacion AS p ON c.poblacion = p.id
    # INNER JOIN audi_manager_pais AS pa ON p.pais = pa.nombre group by pa.nombre;
    for pais in paises_page:
        ventas_count = Venta.objects.filter(
            exposicion__concesionario__poblacion__pais=pais
        ).count()
        num_ventas.append(ventas_count)
    print(num_ventas)
    print(paises_page)
    combined_data = zip(paises_page, num_ventas)
    context = {
        "paises_page": paises_page,
        "combined_data": combined_data,
        "nombre_query": nombre_query,
        "paises_count": paises_list.count(),
    }
    return render(request, "pais/list_paises.html", context)


def list_poblaciones(request):
    is_trabajador = request.session.get("is_trabajador")
    if not is_trabajador:
        # go to login page
        return HttpResponseRedirect("/audi_manager/login/")
    pais_query = request.GET.get("pais", "")
    nombre_query = request.GET.get("nombre", "")
    order = request.GET.get("order", "desc")
    print(order)
    # Query your data using the 'order' parameter
    # ...

    aaugh = ""
    if order != "asc":
        aaugh = "-"

    # QUERY PARA SACAR NUMERO DE VENTAS POR POBLACIÓN
    # SELECT ap.nombre AS poblacion, COUNT(*) AS total_ventas
    # FROM audi_manager_venta AS av
    # JOIN audi_manager_exposicion AS ae ON av.exposicion_id = ae.id
    # JOIN audi_manager_concesionario AS ac ON ae.num_tel_concesionario = ac.num_tel
    # JOIN audi_manager_poblacion AS ap ON ac.poblacion = ap.id GROUP BY ap.nombre;
    poblaciones_list = (
        Poblacion.objects.all()
        .annotate(ventas=Count("concesionario__exposicion__venta"))
        .order_by(f"{aaugh}ventas")
    )

    if pais_query != "":
        poblaciones_list = poblaciones_list.filter(
            Q(pais__nombre__istartswith=pais_query)
        )
    if nombre_query != "":
        poblaciones_list = poblaciones_list.filter(nombre__istartswith=nombre_query)

    # Set the number of items per page
    paginator = Paginator(poblaciones_list, 10)

    page_number = request.GET.get("page")
    poblaciones_page = paginator.get_page(page_number)

    num_ventas = []

    for poblacion in poblaciones_page:
        num_ventas.append(
            Venta.objects.filter(exposicion__concesionario__poblacion=poblacion).count()
        )

    # print(num_ventas)
    # print(poblaciones_page)
    combined_data = zip(poblaciones_page, num_ventas)

    context = {
        "poblaciones_page": poblaciones_page,
        "pais_query": pais_query,
        "nombre_query": nombre_query,
        "combined_data": combined_data,
        "poblaciones_count": poblaciones_list.count(),
        "order": order,
    }
    return render(request, "poblacion/list_poblaciones.html", context)


concesionarios_list = []
original_concesionarios_list = []


def list_concesionarios(request):
    num_tel_query = request.GET.get("num_tel", "")
    poblacion_query = request.GET.get("poblacion", "")
    pais_query = request.GET.get("pais", "")

    # QUERY PARA ORDENAR CONCESIONARIOS POR VALORACION MEDIA
    # SELECT
    #  c.num_tel AS Numero_Telefono,
    #  c.email AS Email,
    #  p.nombre AS Poblacion,
    #  ROUND(AVG(v.rating)::numeric, 3) AS Valoracion_Media
    # FROM
    #  practica.audi_manager_concesionario AS c
    #  LEFT JOIN practica.audi_manager_valoracion AS v ON c.num_tel = v.num_tel_concesionario
    #  JOIN practica.audi_manager_poblacion AS p ON c.poblacion = p.id
    # GROUP BY
    #  c.num_tel,
    #  c.email,
    #  p.nombre
    # ORDER BY
    #  Valoracion_Media DESC;

    # retreive all concesionarios sorted by average rating
    global concesionarios_list
    global original_concesionarios_list

    if len(concesionarios_list) == 0:
        concesionarios_list = Concesionario.objects.annotate(
            avg_rating=Round(Avg("valoracion__rating"), 3),
            ventas=Count("exposicion__venta"),
        ).order_by("-avg_rating")
        original_concesionarios_list = concesionarios_list

    if num_tel_query != "":
        concesionarios_list = concesionarios_list.filter(
            num_tel__istartswith=num_tel_query
        )

    if poblacion_query != "":
        concesionarios_list = concesionarios_list.filter(
            poblacion__nombre__istartswith=poblacion_query
        )

    if pais_query != "":
        concesionarios_list = concesionarios_list.filter(
            poblacion__pais__nombre__istartswith=pais_query
        )

    if num_tel_query == "" and poblacion_query == "" and pais_query == "":
        concesionarios_list = original_concesionarios_list

    paginator = Paginator(concesionarios_list, 20)

    page_number = request.GET.get("page")
    concesionarios_page = paginator.get_page(page_number)

    context = {
        "concesionarios_page": concesionarios_page,
        "concesionarios_count": len(concesionarios_list),
        "num_tel_query": num_tel_query,
        "poblacion_query": poblacion_query,
        "pais_query": pais_query,
    }
    return render(request, "concesionario/list_concesionarios.html", context)


def list_trabajadores(request):
    # Obtener los parámetros de consulta del request
    dni_query = request.GET.get("dni", "")
    name_query = request.GET.get("name", "")
    tipo_query = request.GET.get("tipo", "")
    disponibilidad_query = request.GET.get("disponibilidad", "")

    trabajadores_list = Trabajador.objects.all()
    disponibilidades = sorted(
        list(set([trabajador.disponibilidad for trabajador in trabajadores_list]))
    )
    tipos_trabajador = ["Comercial", "Técnico"]

    if dni_query != "":
        trabajadores_list = trabajadores_list.filter(dni__istartswith=dni_query)
    if name_query != "":
        trabajadores_list = trabajadores_list.filter(Q(nombre__istartswith=name_query))
    if disponibilidad_query != "":
        trabajadores_list = trabajadores_list.filter(
            disponibilidad=disponibilidad_query
        )
    if tipo_query == "Comercial":
        trabajadores_list = trabajadores_list.filter(comercial__isnull=False)
    elif tipo_query == "Técnico":
        trabajadores_list = trabajadores_list.filter(tecnico__isnull=False)

    # Set the number of items per page
    paginator = Paginator(trabajadores_list, 7)

    page_number = request.GET.get("page")
    trabajadores_page = paginator.get_page(page_number)
    context = {
        "trabajadores_page": trabajadores_page,
        "name_query": name_query,
        "dni_query": dni_query,
        "tipo_query": tipo_query,
        "disponibilidad_query": disponibilidad_query,
        "tipos_trabajador": tipos_trabajador,
        "disponibilidades": disponibilidades,
        "trabajadores_count": trabajadores_list.count(),
    }

    return render(request, "trabajador/list_trabajadores.html", context)


def list_tecnicos(request):
    nombre_query = request.GET.get("nombre", "")
    dni_query = request.GET.get("dni", "")
    telefono_query = request.GET.get("telefono", "")
    especializacion_query = request.GET.get("especializacion", "")

    tecnicos_list = Tecnico.objects.all()

    especializaciones = list(
        set([tecnico.especializacion for tecnico in tecnicos_list])
    )

    if nombre_query != "":
        tecnicos_list = tecnicos_list.filter(nombre__istartswith=nombre_query)
    if dni_query != "":
        tecnicos_list = tecnicos_list.filter(dni__istartswith=dni_query)
    if telefono_query != "":
        tecnicos_list = tecnicos_list.filter(num_tel__istartswith=telefono_query)
    if especializacion_query != "":
        tecnicos_list = tecnicos_list.filter(especializacion=especializacion_query)

    paginator = Paginator(tecnicos_list, 10)
    page_number = request.GET.get("page")
    tecnicos_page = paginator.get_page(page_number)

    context = {
        "tecnicos_page": tecnicos_page,
        "nombre_query": nombre_query,
        "dni_query": dni_query,
        "telefono_query": telefono_query,
        "especializaciones": especializaciones,
        "especializacion_query": especializacion_query,
        "tecnicos_count": tecnicos_list.count(),
    }
    return render(request, "tecnico/list_tecnicos.html", context)


def list_comerciales(request):
    lista_comerciales = Comercial.objects.all()
    paginator = Paginator(lista_comerciales, 10)
    page_number = request.GET.get("page")
    comerciales_page = paginator.get_page(page_number)

    context = {
        "comerciales_page": comerciales_page,
        "comerciales_count": lista_comerciales.count(),
    }

    return render(request, "comercial/list_comerciales.html", context)


def list_valoraciones(request):
    # Retrieve user information from the session
    user_id = request.session.get("user_id")

    # Retrieve the user from the database based on the stored user_id
    try:
        user = Persona.objects.get(dni=user_id)
    except Persona.DoesNotExist:
        user = None

    dni_query = request.GET.get("dni", "")
    rating_query = request.GET.get("rating", "")
    concesionario_query = request.GET.get("concesionario", "")

    valoraciones_list = Valoracion.objects.all()
    # Sort by date
    # valoraciones_list = valoraciones_list.order_by("-fecha")

    if dni_query != "":
        valoraciones_list = valoraciones_list.filter(
            cliente__dni__istartswith=dni_query
        )
    if rating_query != "" and rating_query != "-":
        valoraciones_list = valoraciones_list.filter(rating__istartswith=rating_query)
    if concesionario_query != "":
        valoraciones_list = valoraciones_list.filter(
            concesionario__num_tel__istartswith=concesionario_query
        )

    paginator = Paginator(valoraciones_list, 10)
    page_number = request.GET.get("page")
    valoraciones_page = paginator.get_page(page_number)
    context = {
        "valoraciones_page": valoraciones_page,
        "valoraciones_count": valoraciones_list.count(),
        "dni_query": dni_query,
        "rating_query": rating_query,
        "concesionario_query": concesionario_query,
        "user": user,
        "is_trabajador": request.session.get("is_trabajador"),
    }
    return render(request, "valoracion/list_valoraciones.html", context)


def list_vehiculos(request):
    bastidor_query = request.GET.get("bastidor", "")
    matricula_query = request.GET.get("matricula", "")
    ano_query = request.GET.get("ano", "")
    modelo_query = request.GET.get("modelo", "")

    vehiculos_list = Vehiculo.objects.all()
    anos = (
        Vehiculo.objects.values_list("ano_fabricacion", flat=True)
        .distinct()
        .order_by("-ano_fabricacion")
    )
    if bastidor_query != "":
        vehiculos_list = vehiculos_list.filter(num_bastidor__istartswith=bastidor_query)
    if matricula_query != "":
        vehiculos_list = vehiculos_list.filter(matricula__istartswith=matricula_query)
    if ano_query != "":
        vehiculos_list = vehiculos_list.filter(ano_fabricacion=ano_query)
    if modelo_query != "":
        vehiculos_list = vehiculos_list.filter(modelo__istartswith=modelo_query)

    paginator = Paginator(vehiculos_list, 10)
    page_number = request.GET.get("page")
    vehiculos_page = paginator.get_page(page_number)
    print(ano_query)
    context = {
        "vehiculos_page": vehiculos_page,
        "bastidor_query": bastidor_query,
        "matricula_query": matricula_query,
        "ano_query": ano_query,
        "modelo_query": modelo_query,
        "anos": anos,
        "vehiculos_count": vehiculos_list.count(),
    }
    return render(request, "vehiculo/list_vehiculos.html", context)


def list_motores(request):
    motores_list = Motor.objects.all()

    combustibles = list(set([motor.combustible for motor in motores_list]))
    potencias = sorted(list(set([motor.potencia for motor in motores_list])))

    context = {
        "motores_list": motores_list,
        "motores_count": motores_list.count(),
        "combustibles": combustibles,
        "potencias": potencias,
    }
    return render(request, "motor/list_motores.html", context)


def list_exposiciones(request):
    num_tel_query = request.GET.get("num_tel", "")
    numero_query = request.GET.get("numero", "")
    exposiciones_list = Exposicion.objects.all()

    if num_tel_query != "":
        exposiciones_list = exposiciones_list.filter(
            concesionario__num_tel__istartswith=num_tel_query
        )
    if numero_query != "":
        exposiciones_list = exposiciones_list.filter(numero__istartswith=numero_query)

    paginator = Paginator(exposiciones_list, 10)
    page_number = request.GET.get("page")
    exposiciones_page = paginator.get_page(page_number)
    context = {
        "exposiciones_page": exposiciones_page,
        "num_tel_query": num_tel_query,
        "numero_query": numero_query,
        "exposiciones_count": exposiciones_list.count(),
    }

    return render(request, "exposicion/list_exposiciones.html", context)


def list_ventas(request):
    ventas_list = Venta.objects.all()
    paginator = Paginator(ventas_list, 10)
    page_number = request.GET.get("page")
    ventas_page = paginator.get_page(page_number)
    context = {
        "ventas_page": ventas_page,
        "ventas_count": ventas_list.count(),
    }

    return render(request, "venta/list_ventas.html", context)


# ELEMENTS
def persona(request, persona_dni):
    p = get_object_or_404(Persona, dni=persona_dni)

    if request.method == "POST":
        p.nombre = request.POST.get("nombre")
        p.num_tel = request.POST.get("num_tel")
        p.save()
        return HttpResponseRedirect("/audi_manager/personas/")

    context = {"persona": p}
    return render(request, "persona/edit_persona.html", context)


def cliente(request, cliente_dni):
    c = get_object_or_404(Cliente, dni=cliente_dni)

    if request.method == "POST":
        c.dni = request.POST.get("dni")
        c.nombre = request.POST.get("nombre")
        c.num_tel = request.POST.get("num_tel")
        c.email = request.POST.get("email")
        c.save()
        c.persona.save()
        return redirect("/audi_manager/clientes/")

    ventas = Venta.objects.filter(cliente=c)
    vehiculos = Vehiculo.objects.filter(venta__cliente=c)
    valoraciones = Valoracion.objects.filter(cliente=c)

    combined_data = zip(ventas, vehiculos)

    context = {
        "cliente": c,
        "combined_data": combined_data,
        "valoraciones": valoraciones,
    }
    return render(request, "cliente/about_cliente.html", context)


def pais(request, pais_nombre):
    p = get_object_or_404(Pais, nombre=pais_nombre)
    poblaciones = Poblacion.objects.filter(pais=p)
    return render(
        request, "pais/about_pais.html", {"pais": p, "poblaciones": poblaciones}
    )


def poblacion(request, poblacion_pais, poblacion_nombre):
    p = get_object_or_404(
        Poblacion, pais__nombre=poblacion_pais, nombre=poblacion_nombre
    )
    concesionarios = Concesionario.objects.filter(poblacion=p)

    # QUERY PARA SACAR EL CONCESIONARIO CON MÁS VENTAS DE UNA POBLACIÓN
    # SELECT ac.num_tel
    # FROM audi_manager_venta AS av
    # JOIN audi_manager_exposicion AS ae ON av.exposicion_id = ae.id
    # JOIN audi_manager_concesionario AS ac ON ae.num_tel_concesionario = ac.num_tel
    # JOIN audi_manager_poblacion AS ap ON ac.poblacion = ap.id
    # JOIN audi_manager_pais AS apais ON ap.pais = apais.nombre
    # WHERE ap.nombre = 'Port Kevin' AND apais.nombre = 'Russian Federation'
    # GROUP BY ac.num_tel
    # ORDER BY COUNT(*) DESC
    # LIMIT 1;

    # num_tel
    # -----------
    # 904406898

    concesionario_masventas = (
        Concesionario.objects.filter(poblacion=p)
        .annotate(ventas=Count("exposicion__venta"))
        .order_by("-ventas")
        .first()
    )

    return render(
        request,
        "poblacion/about_poblacion.html",
        {
            "poblacion": p,
            "concesionarios": concesionarios,
            "concesionario_masventas": concesionario_masventas,
        },
    )


def concesionario(request, concesionario_num_tel):
    concesionario = get_object_or_404(Concesionario, num_tel=concesionario_num_tel)
    trabajadores = Trabajador.objects.filter(concesionario=concesionario)
    exposiciones = Exposicion.objects.filter(concesionario=concesionario)

    kilometros = sorted(list(set([exposicion.km for exposicion in exposiciones])))
    precios = sorted(list(set([int(exposicion.precio) for exposicion in exposiciones])))

    context = {
        "concesionario": concesionario,
        "trabajadores": trabajadores,
        "exposiciones": exposiciones,
        "kilometros": kilometros,
        "precios": precios,
        "exposiciones_count": exposiciones.count(),
    }

    return render(request, "concesionario/about_concesionario.html", context)


def trabajador(request, trabajador_dni):
    t = get_object_or_404(Trabajador, dni=trabajador_dni)

    # check if exists on comercial or tecnico
    list_comerciales = Comercial.objects.all()
    list_tecnicos = Tecnico.objects.all()

    # query find if exists t.dni in comercial or tecnico
    comercial = list_comerciales.filter(dni=t.dni)
    tecnico = list_tecnicos.filter(dni=t.dni)

    if comercial:
        return HttpResponseRedirect("/audi_manager/comerciales/" + t.dni)
    elif tecnico:
        return HttpResponseRedirect("/audi_manager/tecnicos/" + t.dni)


def tecnico(request, tecnico_dni):
    tecnico = get_object_or_404(Tecnico, dni=tecnico_dni)

    tipos_disponibilidades = ["Mañana", "Tarde", "Completa"]
    tipos_especializacion = ["Mecánica", "Chapa y pintura"]
    vehiculos = Vehiculo.objects.filter(tecnico=tecnico)
    vehiculos_sin_tecnico = Vehiculo.objects.filter(tecnico=None)
    context = {
        "tecnico": tecnico,
        "tipos_disponibilidades": tipos_disponibilidades,
        "tipos_especializaciones": tipos_especializacion,
        "vehiculos": vehiculos,
        "vehiculos_sin_tecnico": vehiculos_sin_tecnico,
        "error_message": "",
    }

    if request.method == "POST":
        try:
            # Update the existing tecnico object with the new data
            tecnico.dni = request.POST["dni"]
            tecnico.nombre = request.POST["nombre"]
            tecnico.num_tel = request.POST["num_tel"]
            tecnico.experiencia = request.POST["experiencia"]
            tecnico.disponibilidad = request.POST["disponibilidad"]
            tecnico.especializacion = request.POST["especializacion"]

            # Save the updated tecnico object
            tecnico.save()
            # delete the original tecnico object
        except Exception as e:
            context["error_message"] = f"Error al actualizar el técnico {e}"
            return render(request, "tecnico/about_tecnico.html", context)

    return render(request, "tecnico/about_tecnico.html", context)


def comercial(request, comercial_dni):
    comercial = get_object_or_404(Comercial, dni=comercial_dni)
    ventas = Venta.objects.filter(comercial=comercial)
    context = {
        "comercial": comercial,
        "ventas": ventas,
    }
    return render(request, "comercial/about_comercial.html", context)


def valoracion(request, cliente_dni, concesionario_num_tel):
    valoracion = get_object_or_404(
        Valoracion,
        cliente__dni=cliente_dni,
        concesionario__num_tel=concesionario_num_tel,
    )
    context = {
        "valoracion": valoracion,
    }
    return render(request, "valoracion/about_valoracion.html", context)


def vehiculo(request, num_bastidor):
    vehiculo = get_object_or_404(Vehiculo, num_bastidor=num_bastidor)
    # exposiciones with the num_bastidor
    exposiciones = Exposicion.objects.filter(vehiculo__num_bastidor=num_bastidor)

    if request.method == "POST":
        try:
            # Update the existing vehiculo object with the new data
            print("editando vehiculo")
            vehiculo.num_bastidor = request.POST["num_bastidor"]
            vehiculo.modelo = request.POST["modelo"]
            # edit existing vehiculo object
            vehiculo.save()
            # go to new vahiculo page
            return HttpResponseRedirect(
                "/audi_manager/vehiculos/" + vehiculo.num_bastidor
            )
        except Exception as e:
            context = {
                "exposiciones": exposiciones,
                "vehiculo": vehiculo,
                "error_message": f"Error al actualizar el vehículo {e}",
            }
            return render(request, "vehiculo/edit_vehiculo.html", context)
    print(vehiculo)
    context = {
        "exposiciones": exposiciones,
        "vehiculo": vehiculo,
    }
    return render(request, "vehiculo/edit_vehiculo.html", context)


def motor(request, motor_combustible, motor_potencia):
    m = get_object_or_404(Motor, combustible=motor_combustible, potencia=motor_potencia)
    vehiculos = Vehiculo.objects.filter(Motor=m).values("modelo").distinct()

    output = (
        "Combustible: %s<br>Potencia: %s<br><br>Modelos que utilizan este tipo de motor:<br>"
        % (m.combustible, m.potencia)
    )
    for vehiculo in vehiculos:
        output += "%s<br>" % vehiculo["modelo"]

    return HttpResponse(output)


def exposicion(request, numero):
    exposicion = get_object_or_404(Exposicion, numero=numero)
    ventas = Venta.objects.filter(exposicion=exposicion)
    context = {
        "exposicion": exposicion,
        "ventas": ventas,
    }
    return render(request, "exposicion/about_exposicion.html", context)


def venta(request, numero):
    venta = get_object_or_404(Venta, numero=numero)
    context = {
        "venta": venta,
    }
    return render(request, "venta/about_venta.html", context)


# ADD
def add_persona(request):
    pass


def add_cliente(request):
    if request.method == "POST":
        try:
            cliente = Cliente(
                dni=request.POST.get("dni"),
                nombre=request.POST.get("nombre"),
                num_tel=request.POST.get("num_tel"),
                username=request.POST.get("username"),
                password=request.POST.get("password"),
                email=request.POST.get("email"),
            )
            cliente.save()
            print(request.POST.get("comercial"))
            # VENTA
            venta = Venta(
                fecha=request.POST.get("fecha").strip(),
                precio_final=request.POST.get("precio_final"),
                exposicion=Exposicion.objects.get(
                    numero=request.POST.get("exposicion")
                ),
                # search num bastidor by exposicion
                vehiculo=Exposicion.objects.get(
                    numero=request.POST.get("exposicion")
                ).vehiculo,
                comercial=Comercial.objects.get(dni=request.POST.get("comercial")),
                cliente=cliente,
            )
            venta.save()

            # VALORACION
            valoracion = Valoracion(
                concesionario=Concesionario.objects.get(
                    num_tel=request.POST.get("concesionario")
                ),
                rating=request.POST.get("rating"),
                cliente=cliente,
                fecha=request.POST.get("fecha").strip(),
            )
            valoracion.save()

        except Exception as e:
            print(e)
    return redirect("list_clientes")


def add_pais(request):
    pass


def add_poblacion(request):
    pass


def add_concesionario(request):
    pass


def add_trabajador(request):
    pass


def add_tecnico(request):
    pass


def add_comercial(request):
    pass


def add_valoracion(request):
    # 915941637
    # 34099455T
    if request.method == "POST":
        try:
            try:
                # buscamos si existe la valoracion para ese cliente y concesionario
                valoracion = Valoracion.objects.get(
                    cliente__dni=request.POST.get("dni"),
                    concesionario__num_tel=request.POST.get("concesionario"),
                )
            except Exception as e:
                print(e)
                # si no existe la valoracion, la creamos (solo se puede hacer una valoracion por cliente y concesionario, guardamos la ultima)
                valoracion = Valoracion(
                    cliente=Cliente.objects.get(dni=request.POST.get("dni")),
                    concesionario=Concesionario.objects.get(
                        num_tel=request.POST.get("concesionario")
                    ),
                )
            # actualizamos los campos no determinantes como el rating y la fecha
            valoracion.rating = request.POST.get("rating")
            valoracion.fecha = request.POST.get("fecha").strip()
            valoracion.save()
        except Exception as e:
            print(e)
    return redirect("list_valoraciones")


def add_vehiculo(request, num_bastidor, dni_tecnico):
    vehiculo = Vehiculo.objects.get(num_bastidor=num_bastidor)
    tecnico = Tecnico.objects.get(dni=dni_tecnico)
    vehiculo.tecnico = tecnico

    vehiculo.save()
    return redirect("tecnico", tecnico_dni=dni_tecnico)


def add_motor(request):
    pass


def add_exposicion(request):
    pass


def add_venta(request):
    pass


# DELETE
def delete_persona(request, dni):
    try:
        persona = Persona.objects.get(dni=dni)
        persona.delete()
    except Exception as e:
        print(e)
    return redirect("list_personas")


def delete_cliente(request, dni):
    try:
        cliente = Cliente.objects.get(dni=dni)
        cliente.delete()
    except Exception as e:
        print(e)
    return redirect("list_clientes")


def delete_pais(request):
    pass


def delete_poblacion(request):
    pass


def delete_concesionario(request):
    pass


def delete_trabajador(request):
    pass


def delete_tecnico(request):
    pass


def delete_comercial(request):
    pass


def delete_valoracion(request, cliente_dni, concesionario_num_tel):
    try:
        valoracion = Valoracion.objects.get(
            cliente__dni=cliente_dni, concesionario__num_tel=concesionario_num_tel
        )
        valoracion.delete()
    except Exception as e:
        print(e)
    return redirect("list_valoraciones")


def delete_vehiculo(request, num_bastidor, dni_tecnico):
    vehiculo = Vehiculo.objects.get(num_bastidor=num_bastidor)
    tecnico = Tecnico.objects.get(dni=dni_tecnico)
    # check if the tecnico is the one who is assigned to the vehiculo
    if vehiculo.tecnico == tecnico:
        vehiculo.tecnico = None
        vehiculo.save()
        print("Vehiculo borrado")
    return redirect("tecnico", tecnico_dni=dni_tecnico)


def delete_motor(request):
    pass


def delete_exposicion(request):
    pass


def delete_venta(request):
    pass


def get_exposicion(request, num_tel):
    exposicion = Exposicion.objects.filter(concesionario__num_tel=num_tel)
    print(exposicion)
    # return value to ajax
    return HttpResponse(",".join([str(elem.numero) for elem in exposicion]))


def get_comercial(request, concesionario_num_tel):
    print("EMTRA AQUI")
    # get all the comercials from the concesionario
    comercial = Comercial.objects.filter(concesionario__num_tel=concesionario_num_tel)

    print(len(comercial))

    # return value to ajax
    return HttpResponse(",".join([str(elem.dni) for elem in comercial]))
