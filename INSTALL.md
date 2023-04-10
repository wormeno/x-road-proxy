## Dependencias
* Python 3

## Instalación

Si se desea ejecutar el sistema como un servicio del SO, en linux seguir los siguientes pasos:
1. Instalar el sistema en el directorio /var/www/html
   * git clone https://github.com/wormeno/x-road-proxy.git

2. Configurar el puerto del sistema. 
   * Archivo SOURCE_APP/src/config/application.properties
     
     * PORT = 8080 (Especificar el puerto asignado al sistema)

3. Ejecutar el programa.
   * python src/index.py runserver 0.0.0.0:8082 

## Instalar el sistema como un servicio del SO (Linux)
* [INSTALL_AS_SERVICE](INSTALL_AS_SERVICE.md)

## Instalar el sistema con docker
* [INSTALL_WITH_DOCKER](INSTALL_WITH_DOCKER.md)
