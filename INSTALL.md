## Dependencias
* Python 3

## Instalación

### Instalación como un servicio del SO en linux
Si se desea ejecutar el sistema como un servicio del SO, en linux seguir los siguientes pasos:
1. Instalar el sistema en el directorio /var/www/html
   * git clone https://github.com/wormeno/x-road-proxy.git

2. Opcional. Configurar el sistema como un servicio del SO (linux)
   1. Copiar el archivo files/x-road-proxy-wsdl.service en el directorio /lib/systemd/system
   2. Revisar que el propietario del archivo sea root y el grupo también
      * sudo chmod 777 /lib/systemd/system/x-road-proxy-wsdl.service
   3. Habilitar el servicio
      * systemctl enable x-road-proxy-wsdl.service

3. Configurar el puerto del sistema. 
   * Archivo SOURCE_APP/src/config/application.properties
     
     * PORT = 8080 (Especificar el puerto asignado al sistema)

4. Ejecutar el programa.
   * python src/index.py runserver 0.0.0.0:8082 
