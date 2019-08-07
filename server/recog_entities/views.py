# Create your views here
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from spacy import displacy
from django.http import JsonResponse
from rdflib.serializer import Serializer
from collections import OrderedDict
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import Counter
# spacy
import spacy
import es_core_news_sm


def loadindex(request):
    # Carga lenguaje español Spacy
    nlp = es_core_news_sm.load()

    my_title = "Caso Arroz Verde"
    texto = ""
    datos = []

    # Se carga el texto de prueba
    if request.method == "POST" and 'prueba' in request.POST:
        texto = request.POST["textoprueba"]
    # Obtiene el texto de entrada
    if request.method == "POST" and 'buscar' in request.POST:
        texto = request.POST["palabraClave"]

    texto = limpiarDatos(texto)
    text = nlp(texto)
    # Tokeniza la entrada de texto con Spacy
    tokenized_sentences = [sentence.text for sentence in text.sents]
    entidadSpacy = []
    # Reconocimiento de entidades con Spacy
    for sentence in tokenized_sentences:
        for entity in nlp(sentence).ents:
            spacyEntidad = entity.text
            entidadSpacy.append(spacyEntidad)
    # Eliminando duplicados en las listas, sin perder el orden
    entidadSpacy = list(set(entidadSpacy))
    # Conteo de entidades
    etiquetaEntidad = []
    count = {}
    claves = []
    valores = []
    dicEntidades = []
    for sentence in entidadSpacy:
        for entity in nlp(sentence).ents:
            entidad = entity.text
            etiqueta = entity.label_
            etiquetaEntidad.append(etiqueta)
            dicEntidades.append({"entidad": entidad, "etiqueta": etiqueta})
    # Conteo de entidades
    count = countDistinct(etiquetaEntidad)
    keyes = count.keys()
    values = count.values()
    for elemento in keyes:
        claves.append(elemento)
    for elemento in values:
        valores.append(elemento)

    palabras_limpias = []
    for enti in entidadSpacy:
        # Limpieza de datos para consulta
        palabra = enti
        palabra = palabra.replace(' ', '_')
        palabra = palabra.replace('á', 'a')
        palabra = palabra.replace('é', 'e')
        palabra = palabra.replace('í', 'i')
        palabra = palabra.replace('ó', 'o')
        palabra = palabra.replace('ú', 'u')
        palabras_limpias.append(palabra)
        datos = listaEntidadesPropias(datos, palabra)
    # Elimina tripletas duplicadas
    datos = OrderedDict((tuple(x), x) for x in datos).values()
    # Valor del texto de entrada
    mis_entidades = texto
    # Imprimir texto con etiquetas de entidades de Spacy
    for enti in palabras_limpias:
        # Saca el indice de cada palabra del arreglo
        indice = palabras_limpias.index(enti)
        

        if indice == len(palabras_limpias):
            break
        else:
            tripletaResultante = anotacion(enti)
            print("triple Salida\t", tripletaResultante)
            if tripletaResultante is not None:
                for uri in tripletaResultante:
                    print("URI encontrada:\t", uri)
                    valorUri = uri.split("/")
                    valorUri = valorUri[len(valorUri)-1]
                    valorUri = valorUri.replace('_', ' ')
                    if valorUri in entidadSpacy[indice]:
                        entidadEtiquetada = '<a href="' + uri + '">' + valorUri + " " + etiquetaEntidad[indice] + "</a>"
                        # Realiza la anotación luego de obtener la URI
                        mis_entidades = mis_entidades.replace(entidadSpacy[indice], entidadEtiquetada)
                        valorUri = displacy.render(text, style="ent")
                    else:
                        print("Texto no relacionado")
            else:
                print("No hay resultados para este entidad")

    var = charts()

    # Diccionario visualizacion en template
    context = {
        'my_title': my_title,
        'claves': claves,
        'valores': valores,
        'dicEntidades': dicEntidades,
        'mis_entidades': mis_entidades,
        'datos': datos,
        'text': var  
    }
    return render(request, "index.html", context)


def info(request):
    return render(request, "info.html", {"title": "¿Como se trabajo?"})


def anotacion(mi_entidad):
    print("llega:\t", mi_entidad)
        
    llegada = mi_entidad.split("_")
    
    
    # Endpoint con Virtuoso
    sbcEndpoint = SPARQLWrapper("http://localhost:8890/sparql/")
    # Consulta SPARQL para buscar en la BD la entidad encontrada
    consulta = """
    SELECT ?s ?p ?o
    WHERE 
    { 
        ?s ?p ?o .
        FILTER (regex(str(?s), "%s") || regex(str(?o), "%s"))
    }""" %  (mi_entidad, mi_entidad)

        

    # Ejecuta la consulta en el Endpoint de Virtuoso
    sbcEndpoint.setQuery(consulta)
    # Retorna en datos JSON
    sbcEndpoint.setReturnFormat(JSON)
    results = sbcEndpoint.query().convert()


    # Dentro del JSON en el atriibuto "results" con el atributo "bindings"
    # Lectura de JSON y division en tripletas
    for result in results["results"]["bindings"]:
        lista = []
        listaS = result["s"]["value"]
        listaP = result["p"]["value"]
        listaO = result["o"]["value"]
        lista.append(listaS)
        lista.append(listaP)
        lista.append(listaO)
        return lista


# Busqueda de la entidad
def listaEntidadesPropias(datos, palabra):
    # Endpoint con Virtuoso
    sbcEndpoint = SPARQLWrapper("http://localhost:8890/sparql/")
    # Consulta SPARQL para buscar en la BD la entidad encontrada
    consulta = """
        SELECT ?s ?p ?o
        WHERE 
        { 
            ?s ?p ?o .
            FILTER (regex(str(?s), "%s") || regex(str(?o), "%s"))
        }
        """ % (palabra, palabra)

    # Ejecuta la consulta en el Endpoint de Virtuoso
    sbcEndpoint.setQuery(consulta)
    # Retorna en datos JSON
    sbcEndpoint.setReturnFormat(JSON)
    results = sbcEndpoint.query().convert()

    # Dentro del JSON en el atriibuto "results" con el atributo "bindings"
    # Lectura de JSON y division en tripletas
    for result in results["results"]["bindings"]:
        lista = []
        listaS = result["s"]["value"]
        listaP = result["p"]["value"]
        listaO = result["o"]["value"]
        lista.append(listaS)
        lista.append(listaP)
        lista.append(listaO)
        datos.append(lista)
        # print("Funcion:\t", lista)
    return datos
# Busqueda de la entidad
def charts():
    # Endpoint con Virtuoso
    sbcEndpoint = SPARQLWrapper("http://localhost:8890/sparql/")
    # Consulta SPARQL para buscar en la BD la entidad encontrada
    consulta = """
        PREFIX cavr:<http://localhost:8080/negociador/resource/>
        SELECT (COUNT(?personas) AS ?NumPersonas), (COUNT(?empresas) AS ?NumEmpresas), (COUNT(?paises) AS ?NumPais), (COUNT(?casos) AS ?NumCaso), (COUNT(?provincias) AS ?NumProvincia)
        WHERE
        {
            {?personas rdf:type cavr:Persona. }
            union
            {?empresas rdf:type cavr:Empresa.}
            union
            {?paises rdf:type cavr:Pais.}
            union
            {?casos rdf:type cavr:Caso.}
            union
            {?provincias rdf:type cavr:Provincia.}
        }
        """ 

    # Ejecuta la consulta en el Endpoint de Virtuoso
    sbcEndpoint.setQuery(consulta)
    # Retorna en datos JSON
    sbcEndpoint.setReturnFormat(JSON)
    results = sbcEndpoint.query().convert()
    print("GRAFICA\T", results)
    # Dentro del JSON en el atriibuto "results" con el atributo "bindings"
    # Lectura de JSON y division en tripletas
    datos = []
    for result in results["results"]["bindings"]:
        listaP = result["NumPersonas"]["value"]
        listaE = result["NumEmpresas"]["value"]
        listaL = result["NumPais"]["value"]
        listaC = result["NumCaso"]["value"]
        listaPV = result["NumProvincia"]["value"]
        datos.append({"key": "NumPersonas", "value": listaP})
        datos.append({"key": "NumEmpresas", "value": listaE})
        datos.append({"key": "NumPais", "value": listaL})
        datos.append({"key": "NumCaso", "value": listaC})
        datos.append({"key": "NumProvincia", "value": listaPV})
        # print("Funcion:\t", lista)
    return datos




# Limpieza texto de entrada
def limpiarDatos(palabra):
    palabra = str(palabra)
    palabra = palabra.replace('—', '')
    palabra = palabra.replace('á', 'a')
    palabra = palabra.replace('é', 'e')
    palabra = palabra.replace('í', 'i')
    palabra = palabra.replace('ó', 'o')
    palabra = palabra.replace('ú', 'u')
    return palabra


def countDistinct(arr):
    # counter method gives dictionary of elements in list
    # with their corresponding frequency.
    # using keys() method of dictionary data structure
    # we can count distinct values in array
    return Counter(arr)
