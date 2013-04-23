Title: Crea tu propia distro de Linux con Yocto
Tags: yocto, poky, distribución
Date: 2013-01-22
PlusActivityId: z13agjmr0tazhfwft22egliyvmyrubrkf

El objetivo de este artículo es explicar paso a paso como se puede utilizar
el proyecto [Yocto] para crear nuestra propia distribución de Linux. Primero
construiremos una para ejecutarla en [QEMU] y después otra para nuestra
Raspberry Pi.

## Inicio rápido

El inicio rápido con el proyecto [Yocto] está perfectamente documentado en
[Yocto Project Quick Start]. En cualquier caso aquí resumiremos los pasos
deteniéndonos en los de mayor importancia.

### Requisitos

 * **Una distribución de Linux.** En nuestro caso, por simplicidad, cualquiera
de las basadas en Debian.
 * **Paquetes de desarrollo.** En el sistema deben estar instalados una serie
de paquetes utilizados habitualmente en tareas de desarrollo. En un sistema
basado en Debian deberían poder instalarse con el siguiente comando:

        :::sh
        $ sudo apt-get install sed wget cvs subversion git-core \
        coreutils unzip texi2html texinfo libsdl1.2-dev docbook-utils \
        gawk python-pysqlite2 diffstat help2man make gcc \
        build-essential g++ desktop-file-utils chrpath libgl1-mesa-dev \
        libglu1-mesa-dev mercurial autoconf automake groff

 * **Una versión del proyecto [Yocto].** Las distintas versiones pueden
descargarse desde la dirección:

    [http://downloads.yoctoproject.org/releases/yocto/](http://downloads.yoctoproject.org/releases/yocto/)

### Construir una imagen de sistema Linux

El proceso de construir una imagen genera una distribución de Linux completa,
incluyendo las herramienta de desarrollo para la misma:

 1. Descargar el sistema de construcción [Poky] de la última versión del
proyecto [Yocto] y descomprimirla:

        :::sh
        $ wget http://downloads.yoctoproject.org/releases/yocto/yocto-1.3/poky-danny-8.0.tar.bz2
        $ tar jxf poky-danny-8.0.tar.bz2

 2. Crear el directorio `raspberry-pi-build` donde construir la imagen y
configurar las variables de entorno necesarias:

        :::sh
        $ source poky-danny-8.0/oe-init-build-env raspberry-pi-build

     Como las variables de entorno configuradas por este comando se pierden al
     cerrar la shell, en caso de que eso ocurra o de abandonar la sesión sería
     necesario volver a ejecutar este comando antes de continuar.

 3. Construir la imagen:

        :::sh
        $ bitbake core-image-minimal

La imagen construida puede ejecutarse en [QEMU] de la siguiente manera:

    :::sh
    $ runqemu qemux86

Y en unos segundos tendremos acceso a la consola de nuestra nueva distribución.

### Optimizando la construcción

En el archivo `conf/local.conf` del directorio `raspberry-pi-build` se pueden
definir algunos parámetros que pueden reducir el tiempo necesario para
construir la imagen si se dispone de un sistema multi-núcleo.

Si se tienen `N` núcleos, es conveniente descomentar las variables `BB_NUMBER_THREADS`
y `PARALLEL_MAKE` y asignarle `N + 1`. Por ejemplo, con 8 núcleos el valor
debería ser 9:

    BB_NUMBER_THREADS = "9"
    PARALLEL_MAKE = "-j 9"

## Crear una distribución para Raspberry Pi

El ejemplo estándar del proyecto [Yocto] se construye por defecto para la arquitectura
**qemux86**. En el caso de querer compilar para otro sistema sólo es necesario añadir
una capa que incorpore los archivos de configuración necesarios.

En nuestro caso dicha capa es **meta-raspberrypi**, una capa [BSP] que agrupa todos los
metadatos necesarios para construir para dispositivos Raspberry Pi. Fundamentalmente
contiene configuraciones para el núcleo y opciones para la arquitectura.

Estos son los pasos para incorporarla a nuestro proyecto:

 1. Clonar localmente el repositorio **meta-raspberrypi** fuera del directorio
`raspberry-pi-build`.

        :::sh
        $ git clone https://github.com/djwillis/meta-raspberrypi.git

 2. Cambiar a la rama **danny** que es la de la versión de [Poky] que estamos usando:

        :::sh
        $ cd meta-raspberrypi
        $ git checkout danny

 3. Buscar la variable `BBLAYERS` en `raspberry-pi-build/conf/bblayers.conf` y añadir
al final la ruta hasta el repositorio de la capa **meta-raspberrypi** para incluirla
en el proceso de construcción. Por ejemplo:

        BBLAYERS ?= " \
          /home/usuario/poky-danny-8.0/meta \
          /home/usuario/poky-danny-8.0/meta-yocto \
          /home/usuario/poky-danny-8.0/meta-yocto-bsp \
          /home/usuario/meta-raspberry-pi \
        "

 4. Buscar la variable `MACHINE` en `raspberry-pi-build/conf/local.conf` e indicar que
la máquina de destino de la imagen es `raspberrypi`

        MACHINE ?= "raspberrypi"

 5. Construir la imagen:

        :::sh
        $ cd raspberry-pi-build
        $ bitbake rpi-basic-image

    Esta imagen incluye un servidor **SSH** y un _splash_ de Raspberry Pi durante el arranque.
Mientras que la imagen alternativa `rpi-hwup-image` no contiene ninguna de las dos cosas.
    
 6. Transferir la imagen construida a la tarjeta SD.

        :::sh
        $ sudo dd if=tmp/deploy/images/rpi-basic-image-raspberrypi.rpi-sdimg of=/ruta/a/la/sd

    y probarla en el dispositivo.

## Referencias

 1. [Yocto Project Quick Start](http://www.yoctoproject.org/docs/1.0/yocto-quick-start/yocto-project-qs.html).
 1. [Poky HandBook](http://pokylinux.org/doc/poky-handbook.html).
 1. [Build a Custom Raspberry Pi Distro with OpenEmbedded & Yocto](http://www.pimpmypi.com/blog/blogPost.php?blogPostID=7).

[Yocto]: |filename|/Overviews/yocto-poky-y-bitbake.md "Yocto, Poky y BitBake"
[Poky]: |filename|/Overviews/yocto-poky-y-bitbake.md "Yocto, Poky y BitBake"
[Yocto Project Quick Start]: http://www.yoctoproject.org/docs/1.0/yocto-quick-start/yocto-project-qs.html "Yocto Project Quick Start"
[QEMU]: http://wiki.qemu.org/ "QEMU"
[BSP]: http://en.wikipedia.org/wiki/Board_support_package "Board Support Package"
