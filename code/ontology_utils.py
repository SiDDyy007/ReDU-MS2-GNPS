
import json
from security import safe_requests

"""Resolving ontologies only if they need to be"""
def resolve_ontology(attribute, term):

    if attribute == "ATTRIBUTE_BodyPart":
        url = "https://www.ebi.ac.uk/ols/api/ontologies/uberon/terms?iri=http://purl.obolibrary.org/obo/%s" % (term.replace(":", "_"))
        try:
            safe_requests.get(url)
            ontology_json = json.loads(safe_requests.get(url).text)
            #print(json.dumps(ontology_json))
            return ontology_json["_embedded"]["terms"][0]["label"]
        except KeyboardInterrupt:
            raise
        except:
            return term

    if attribute == "ATTRIBUTE_Disease":
        url = "https://www.ebi.ac.uk/ols/api/ontologies/doid/terms?iri=http://purl.obolibrary.org/obo/%s" % (term.replace(":", "_"))
        try:
            ontology_json = safe_requests.get(url).json()
            return ontology_json["_embedded"]["terms"][0]["label"]
        except KeyboardInterrupt:
            raise
        except:
            return term

    if attribute == "ATTRIBUTE_DatasetAccession":
        try:
            url = f"https://massive.ucsd.edu/ProteoSAFe//proxi/v0.1/datasets?filter={term}&function=datasets"
            dataset_information = safe_requests.get(url).json()
            return dataset_information["title"]
        except KeyboardInterrupt:
            raise
        except:
            return "Not Available"
            #raise Exception(url)

    return term
