import requests
import os


def xbrl_request(cvrs):
    """
    POST request to XBRL endpoint based on CVRs. Max. 2999 hits returned. Max. of ~200000 CVRs to query.
    """
    xbrl_endpoint = "http://distribution.virk.dk/offentliggoerelser/_search"

    headers = {
        'Content-Type': 'application/json',
    }

    query_body = {

        "query": {
            "bool": {

                "must": [

                    {

                        "term": {

                            "dokumenter.dokumentMimeType": "application"

                        }

                    },

                    {

                        "term": {

                            "dokumenter.dokumentMimeType": "xml"

                        }

                    },
                    {

                        "range": {

                            "regnskab.regnskabsperiode.slutDato": {

                                "gt": "2019-01-01T00:00:00.001Z"

                            }

                        }

                    }

                ],
                "filter": {
                    "terms": {
                        "cvrNummer": cvrs
                    }
                }
                ,

                "must_not": [],

                "should": []

            }

        },

       "size": 2999

    }

    query = str(query_body).replace('\'', '\"')

    response = requests.post(xbrl_endpoint, headers = headers, data = query)
    
    return(response)


def get_xml(url, cvrnummer, slutdato, xml_outpath):
    """
    Download XML-file based on URL. "cvrnummer" and "slutdato" used for filename.
    """
    xml = requests.get(url).text
    filename = "{cvr}_{dato}.xml".format(cvr = cvrnummer, dato = slutdato)
    xmlout = os.path.join(xml_outpath, filename)
    
    with open(xmlout, 'w', encoding = 'utf-8') as f:
        f.write(xml)