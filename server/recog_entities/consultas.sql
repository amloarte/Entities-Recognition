PREFIX cavr: <http://localhost:8080/negociador/page/>
select * where {

?s cavr:apellido ?o .
}


for sentence in tokenized_sentences:
        for entity in self.nlp(sentence).ents:
            entidades.append(entity.text)
            palabra = self.limpiarDatos(entity)
            consultatype = """
            PREFIX cavr: <http://localhost:8080/negociador/page/>
                select * where {

                ?s cavr:apellido ?o .
                }
                    """ % (palabra,palabra)
            print("la palabra es:",palabra )
            self.sbcEndpoint.setQuery(consultatype)
            # retornar consulta enformto json
            self.sbcEndpoint.setReturnFormat(JSON)
            results = self.sbcEndpoint.query().convert()
            for result in results["results"]["bindings"]:
                listae = []
                listaSe = result["s"]["value"]
                #listaPe = result["p"]["value"]
                listaOe = result["o"]["value"]
                listae.append(listaSe)
                #listae.append(listaPe)
                listae.append(listaOe)
                datostype.append(listae)
                print("los datos   : " , datostype)
    return datos, entidades,datostype


     PREFIX cavr:<http://localhost:8080/negociador/resource/>
SELECT *
WHERE 
{ 
                {?s  cavr:nombre ?o .}  
                UNION
                {?s cavr:segundoApellido ?o .}
                UNION
                {?s  cavr:codigoPersona ?o .} 
                UNION
                {?s  cavr:nombradoPor  ?o .} 
                 UNION
                {?s  cavr:nombreProvincia ?o .} 
                UNION
                {?s  cavr:liderImplicado ?o .} 
                UNION
                {?s  cavr:Persona ?o .}
                UNION
                {?s  cavr:detenidoEn ?o .}
UNION
                {?s  cavr:involucrada ?o .} 
UNION
                {?s  cavr:type ?o .}
UNION 
                {?s  cavr:asignacionCodigo ?o .}
UNION 
                {?s  cavr:codigoEmpresa ?o .} 
UNION 
                {?s  cavr:nombreEmpresa ?o .}
UNION 
                {?s  cavr:recauda ?o .}
                
        }



        PREFIX cavr:<http://localhost:8080/negociador/resource/>
        SELECT *
        WHERE 
        { 
                {?s  cavr:nombre ?o .FILTER (regex(str(?o), "%s")) .}  
                UNION
                {?s cavr:segundoApellido ?o .FILTER (regex(str(?o), "%s")) .}
                UNION
                {?s  cavr:codigoPersona ?o .FILTER (regex(str(?o), "%s")) .} 
                UNION
                {?s  cavr:nombradoPor  ?o .FILTER (regex(str(?o), "%s")) .} 
                 UNION
                {?s  cavr:nombreProvincia ?o .FILTER (regex(str(?o), "%s")) .} 
                UNION
                {?s  cavr:liderImplicado ?o .FILTER (regex(str(?o), "%s")) .} 
                UNION
                {?s  cavr:Persona ?o .FILTER (regex(str(?o), "%s")) .}
                UNION
                {?s  cavr:detenidoEn ?o .FILTER (regex(str(?o), "%s")) .} 
                
        }


        SPARQL CLEAR GRAPH <miOnt:move>


        PREFIX cavr:<http://localhost:8080/negociador/resource/>
        SELECT *
        WHERE 
        { 
                {?s  cavr:nombre ?o .FILTER (regex(str(?o), "%s")) .}  
                UNION
                {?s cavr:segundoApellido ?o .FILTER (regex(str(?o), "%s")) .}
                UNION
                {?s  cavr:codigoPersona ?o .FILTER (regex(str(?o), "%s")) .} 
                UNION
                {?s  cavr:nombradoPor  ?o .FILTER (regex(str(?o), "%s")) .} 
                 UNION
                {?s  cavr:nombreProvincia ?o .FILTER (regex(str(?o), "%s")) .} 
                UNION
                {?s  cavr:liderImplicado ?o .FILTER (regex(str(?o), "%s")) .} 
                UNION
                {?s  cavr:Persona ?o .FILTER (regex(str(?o), "%s")) .}
                UNION
                {?s  cavr:detenidoEn ?o .FILTER (regex(str(?o), "%s")) .}
                UNION
                {?s  cavr:involucrada ?o .FILTER (regex(str(?o), "%s")) .} 
                UNION
                {?s  rdf:type ?o .FILTER (regex(str(?o), "%s")) .}
                UNION 
                {?s  cavr:asignacionCodigo ?o .FILTER (regex(str(?o), "%s")) .}
                UNION 
                {?s  cavr:codigoEmpresa ?o .FILTER (regex(str(?o), "%s")) .} 
                UNION 
                {?s  cavr:nombreEmpresa ?o .FILTER (regex(str(?o), "%s")) .}
                UNION 
                {?s  cavr:recauda ?o .FILTER (regex(str(?o), "%s")) .}
                
        }e