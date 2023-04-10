### Instalación como un servicio del SO en linux

Si se desea ejecutar el sistema como un servicio del SO, en linux seguir los siguientes pasos:

1. Configurar el sistema como un servicio del SO (linux)
   1. Copiar el archivo files/x-road-proxy-wsdl.service en el directorio /lib/systemd/system
   2. Revisar que el propietario del archivo sea root y el grupo también
      * sudo chmod 777 /lib/systemd/system/x-road-proxy-wsdl.service
   3. Habilitar el servicio
      * systemctl enable x-road-proxy-wsdl.service

2. Ejecutar el sistema
   * systemctl start x-road-proxy-wsdl.service
