### Instalación con docker

1. Configurar el puerto. Debe ser el mismo que se indica en el archivo config/application.properties
   * En el archivo docker-compose.yml:
     * command: python src/xroad_proxy_wsdl.py runserver 0.0.0.0:8080
     * ports:
      - "8080:8080"
2. Ejecutar el programa
   * docker-compose up -d