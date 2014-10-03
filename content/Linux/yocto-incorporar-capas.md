Title: Incorporar funcionalidad a Yocto mediante capas. Un ejemplo con Qt
Tags: yocto, poky, distribución, qt, gui, capas
Date: 2013-01-30

Una vez hemos [construido nuestra distribución](|filename|/Linux/crear-una-distro-linux-con-yocto.md) podemos incorporarle nuevas funcionalidades a través de **capas**.

Las capas no son más que grupos de recetas, cada una de las cuales contiene
información sobre como construir un componente de software concreto, de manera
que trabajando juntos se incorpora la funcionalidad deseada. Para nuestro ejemplo
añadiremos a nuestra distribución el _framework_ de desarrollo de aplicaciones [Qt](|filename|/Overviews/proyecto-qt.md).

La versión actual del proyecto [Yocto] ya provee de la capa **meta-qt** que
permite incluir [Qt 4.8 Embedded for Linux](http://doc.qt.digia.com/main-snapshot/qt-embedded-linux.html) en nuestra distribución.

Sin embargo en la versión 5 se actualiza y reemplaza _[Qt] for Embedded Linux_ con un
nuevo componente denominado [QPA] o _Qt Platform Abstraction_. La nueva arquitectura
es más simple, facilita la integración de [Qt] con cualquier sistema de ventanas
—suprime el gestor de ventanas QWS incluido en _[Qt] for Embedded Linux_— y la
inclusión de contenidos basados en [OpenGL]. Por eso la 5 será la versión que
utilizaremos en nuestro proyecto.

En [una charla de Thomas Senyk](http://qt-project.org/videos/watch/qpa-the-qt-platform-abstraction)
se desarrollan mucho mejor todas estas diferencias y se justifican las ventajas
de QPA respecto a su predecesor.

## Incorporar Qt

Incorporar [Qt] es muy similar a hacerlo para [el soporte de Raspberry Pi](|filename|/Linux/crear-una-distro-linux-con-yocto.md) a nuestra distribución:

 1. Clonar localmente el repositorio **meta-qt5** fuera del directorio `raspberry-pi-build`.

        :::sh
        $ git clone https://github.com/meta-qt5/meta-qt5.git

 2. Buscar la variable `BBLAYERS` en `raspberry-pi-build/conf/bblayers.conf` y añadir
al final la ruta hasta el repositorio de la capa **meta-qt5** para incluirla
en el proceso de construcción. Por ejemplo:

        BBLAYERS ?= " \
          /home/usuario/poky-danny-8.0/meta \
          /home/usuario/poky-danny-8.0/meta-yocto \
          /home/usuario/poky-danny-8.0/meta-yocto-bsp \
          /home/usuario/meta-raspberry-pi \
          /home/usuario/meta-qt5 \
        "

 3. Construir la imagen del sistema:

        :::sh
        $ cd raspberry-pi-build
        $ bitbake rpi-basic-image

    Recuerda que esta imagen incluye un servidor **SSH** y un _splash_ de Raspberry Pi durante el arranque.
Mientras que la imagen alternativa `rpi-hwup-image` no contiene ninguna de las dos cosas.
    
 4. Transferir la imagen construida a la tarjeta SD:

        :::sh
        $ sudo dd if=tmp/deploy/images/rpi-basic-image-raspberrypi.rpi-sdimg of=/ruta/a/la/sd

    y probarla en el dispositivo.

## Referencias

 1. [Yocto Project Quick Start](http://www.yoctoproject.org/docs/1.0/yocto-quick-start/yocto-project-qs.html).

[QPA]: http://qt-project.org/wiki/Qt-Platform-Abstraction "Qt Platform Abstraction"
[Yocto]: |filename|/Overviews/yocto-poky-y-bitbake.md "Yocto, Poky y BitBake"
[Qt]: |filename|/Overviews/proyecto-qt.md "Proyecto Qt. Framework de desarrollo de aplicaciones"
[OpenGL]: http://es.wikipedia.org/wiki/OpenGL "OpenGL"