# Create your views here
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

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

    # Endpoint con Virtuoso
    sbcEndpoint = SPARQLWrapper("http://localhost:8890/sparql/")
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
            entidadSpacy.append(entity.text)
    
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
    count = countDistinct(etiquetaEntidad)
    keyes = count.keys()
    values = count.values()
    print(count)
    for elemento in keyes:
        claves.append(elemento)
        print("elemento\t", elemento)
    for elemento in values:
        valores.append(elemento)
        print("elemento\t", elemento)
    
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

        # Consulta SPARQL para buscar en la BD la entidad encontrada
        consulta = """
            SELECT ?s ?p ?o
            FROM <http://localhost:8890/Arroz>
            WHERE 
            { 
                ?s ?p ?o .FILTER (regex(str(?s), "%s") || regex(str(?o), "%s")) .
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
            entidadEtiquetada = '<a class="badge badge-info" href="http://localhost:8080/negociador/page/' + enti + '">' + entidadSpacy[indice]+"</a>"
        # prUnder(entidadEncontrada)
        # prIN(entidadEncontrada, etiqueta)
            mis_entidades = mis_entidades.replace(
            entidadSpacy[indice], entidadEtiquetada)

    
    #Diccionario visualizacion en template
    context = {
        'my_title': my_title,
        'claves': claves,
        'valores': valores,
        'dicEntidades': dicEntidades,
        'mis_entidades': mis_entidades,
        'datos': datos
    }
    return render(request, "index.html", context)


def info(request):
    return render(request, "info.html", {"title": "¿Como se trabajo?"})

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
