import logging
import requests
from bs4 import BeautifulSoup
from lxml.html import HTMLParser


class SoapConsumer:

    def process_request(self, request):
        """
        Consume el servicio soap requerido
        Retorna la respuesta con los headers informados, necesarios para x-road
        """

        logging.info("\r\n Iniciando proceso")
        xml_request = request.body
        url_ws = request.protocol + ":/" + request.uri

        try:
            req = requests.Request('POST', url_ws,
                                   data=xml_request)
        except requests.RequestException as e:
            raise e

        prepped_requ = req.prepare()

        s = requests.Session()
        xml_response = s.send(prepped_requ)

        result = self.__parse_xml(xml_request, xml_response.content)
        return result

    def __parse_xml(self, xml_request, xml_response):
        """
        Reemplaza el xml_request.body por el xml_response.body
        """
        xml_request = BeautifulSoup(xml_request, 'xml')

        xml_response = BeautifulSoup(xml_response, 'xml')
        xml_response = self.__add_envelop_source_to_target(xml_request, xml_response)
        xml_response = self.__add_header_source_to_target(xml_request, xml_response)
        # xml_request.Body.clear()
        # for child in xml_response.Body:
        #     xml_request.Body.append(child)
        print(xml_response)
        return xml_response

    def __add_envelop_source_to_target(self, source_xml, target_xml):
        """
        source_xml= BeautifulSoup
        target_xml= BeautifulSoup
        Agrega los atributos del source_xml al target_xml
        """
        print("\r\n procesando Envelope\r\n")

        for atr in source_xml.Envelope.attrs:
            target_xml.Envelope[atr] = source_xml.Envelope.attrs[atr]

        return target_xml

    def __add_header_source_to_target(self, source_xml, target_xml):
        """
        source_xml= BeautifulSoup
        target_xml= BeautifulSoup
        Agrega el header definido en el source_xml al target_xml
        """
        print("\r\n procesando Header\r\n")
        if target_xml.Header is None:
            target_xml.Envelope.append(source_xml.Header)
        else:
            for child in source_xml.Header:
                target_xml.Envelope.Header.extend(child)

        return target_xml


    def __validar_xml_request(self, xml_request):
        try:
            xml_request.Envelop.attrs
        except HTMLParser.HTMLParseError as e:
            print("error")
            print(e)
