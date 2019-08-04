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