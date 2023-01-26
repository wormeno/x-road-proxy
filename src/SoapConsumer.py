import logging
import requests
from bs4 import BeautifulSoup


def value_is_empty(value):
    return value is None or value == ''


def value_ci_in_array(value, array):
    return len(list(filter(lambda item: item.upper() == value.upper(), array))) > 0


class SoapConsumer:

    def process_request(self, request):
        """
        Consume el servicio soap requerido
        Retorna la respuesta con los headers informados, necesarios para x-road
        """
        logging.info("Process request...")

        xml_request = request.body
        url_ws = request.protocol + ":/" + request.uri

        logging.info("Service provider: " + url_ws)

        headers = HeaderValido().get_header_valido(request.headers)

        try:
            req = requests.Request('POST', url_ws, headers=headers, data=xml_request)
        except requests.RequestException as e:
            raise e

        xml_response = requests.Session().send(req.prepare())

        return Xml().get_response_xml(xml_request, xml_response.content, xml_response.status_code)


class HeaderValido:
    """
        Retorna el header valido para enviar al cliente soap
        Elimina del header original, los valores agregados por x-road y aquellos headers que no informan valor
    """

    headers_no_validos = ["Host", "Transfer-Encoding"]

    def get_header_valido(self, un_header):
        return dict(filter(self.__filtered_in_array, un_header.items()))

    def __filtered_in_array(self, pair):
        key, value = pair
        if value_is_empty(value):
            return False
        return value_ci_in_array(key, self.headers_no_validos) is False


class Xml:
    """
        Arma la respuesta agregando los headers requeridos por x-road
        Si el service provider no retorna xml valido => se crea un xml incorporando la respuesta del service provider
    """

    def get_response_xml(self, xml_request, xml_response, response_status_code):
        """
        xml_request: xml enviado en el request body
        xml_response: respuesta xml del servicio soap
        Reemplaza el xml_request.body por el xml_response.body
        """
        logging.info("Init process parser response xml...")
        xml_request = BeautifulSoup(xml_request, 'xml')

        xml_response = self.__get_beautiful_soup_xml(xml_response, response_status_code)

        xml_response = self.__add_envelop_source_to_target(xml_request, xml_response)
        xml_response = self.__add_header_source_to_target(xml_request, xml_response)

        logging.info("process parser response xml Ok!")

        return xml_response

    def __get_beautiful_soup_xml(self, response_xml, response_status_code):
        xml = BeautifulSoup(response_xml, 'xml')
        if self.__validar_xml(xml):
            return xml
        else:
            return self.__get_xml_fault(response_xml, response_status_code)

    def __add_envelop_source_to_target(self, source_xml, target_xml):
        """
        source_xml= BeautifulSoup
        target_xml= BeautifulSoup
        Agrega los atributos del source_xml al target_xml
        """

        logging.info("Init add envelope source to response..")

        for atr in source_xml.Envelope.attrs:
            target_xml.Envelope[atr] = source_xml.Envelope.attrs[atr]

        logging.info("Add envelope to response Ok!")

        return target_xml

    def __add_header_source_to_target(self, source_xml, target_xml):
        """
        source_xml= BeautifulSoup
        target_xml= BeautifulSoup
        Agrega el header definido en el source_xml al target_xml
        """

        logging.info("Init source header to response...")

        if target_xml.Header is None:
            target_xml.Envelope.append(source_xml.Header)
        else:
            for child in source_xml.Header:
                target_xml.Envelope.Header.extend(child)

        logging.info("Source header to response Ok!")

        return target_xml

    def __validar_xml(self, source_xml):
        return source_xml.contents is not None and source_xml.contents

    def __get_xml_fault(self, fault_response, status_code):
        xml = '<?xml version="1.0" encoding="UTF-8"?>\r\n' \
              ' <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" >\r\n ' \
              '    <soap:Body>\r\n' \
              '        <soap:Fault>\r\n' \
              '            <faultcode>soap:Server</faultcode>\r\n' \
              '            <faultstring>ServiceProvider response status_code (' + str(status_code) + '): ' + str(
            fault_response) + '</faultstring>\r\n' \
                              '              <detail />\r\n' \
                              '        </soap:Fault> \r\n' \
                              '    </soap:Body> \r\n' \
                              '</soap:Envelope>\r\n'
        xml_beauty = BeautifulSoup(xml, 'xml')
        return xml_beauty
