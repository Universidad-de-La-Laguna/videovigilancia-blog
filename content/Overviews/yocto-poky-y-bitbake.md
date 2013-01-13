Title: Yocto, Poky y BitBake
Tags: yocto, poky, bitbake, empotrado, linux, openembedded
Author: Jesús Torres
Date: 2013-01-10

El proyecto [Yocto] proporciona a los desarrolladores de sistemas empotrados
Linux un punto de partida para generar distribuciones personalizadas para
sus productos. Una de las piezas clave del proyecto es el sistema de
construcción [Poky], que a su vez se apoya en [BitBake], una herramienta de
construcción de paquetes al estilo de
[Portage](http://es.wikipedia.org/wiki/Portage_(software)) de
[Gentoo](http://www.gentoo.org/).

## El proyecto Yocto

[Yocto] está financiado por la [Linux Foundation](http://www.linuxfoundation.org/).
Su principal objetivo es desarrollar herramientas que ayuden a los desarrolladores
a crear sus propias distribuciones de Linux, sea cual sea el hardware sobre el que
van a correr. Entre los proyectos desarrollados en el seno de [Yocto] están:
el sistema de construcción [Poky], el sistema de
[integración continua](http://es.wikipedia.org/wiki/Integraci%C3%B3n_continua)
[Autobuiler](http://autobuilder.yoctoproject.org/) y la librería de sistema
[Embedded GLIBC (EGLIBC)](http://www.eglibc.org/).

Además, cuando se crea una distribución con [Yocto], la herramienta de construcción
crea un SDK de desarrollo de aplicaciones adaptado a dicha distribución. Este
SDK puede conectarse al IDE [Eclipse] o puede usarse desde la línea de comandos.

## El sistema de construcción Poky

Uno de los componentes centrales de [Yocto] es el sistema de construcción [Poky].
Su responsabilidad fundamental es la construcción de imágenes de sistemas de
archivos de sistemas Linux. Estos pueden incluir diferentes productos de software:
Linux, X11, Matchbox, GTK+, Pimlico, Clutter, D-BUS, etc.

Aunque se pueden generar diferentes tipos de imágenes según el dispositivo donde
va a ser almacenada, el proyecto ejemplo estándar lo hace para el emulador [QEMU]
y para placas de referencia reales de los fabricantes, para cada una de las
arquitecturas soportadas. Esta habilidad de [Poky] lo hace especialmente
apropiado como plataforma de pruebas y de desarrollo de software para empotrados.

Un proyecto similar a [Poky] es [OpenEmbedded], que también es un sistema de construcción
para sistemas Linux empotrados. [Poky] deriva de un proyecto para crear
una rama estabilizada de [OpenEmbedded], limitando el software disponible a unos
pocos paquetes, de entre los miles de los que dispone [OpenEmbedded], así como el número
de arquitecturas soportadas. Con el tiempo esta rama evolucionó añadiendo
el componente de [Eclipse] y la generación de imágenes para [QEMU], entre otras cosas.
Esto dio origen a [Poky].

El núcleo central de [Poky] es la herramienta de construcción [BitBake] junto
con una colección de archivos de configuración de diversos tipos que definen
todo lo necesario para construir la imagen del sistema Linux.

## La herramienta de construcción BitBake

[BitBake] es básicamente un ejecutor de tareas. Su función es leer los archivos
de configuración que definen el proyecto; establecer que tareas deben ser realizadas
y en que orden, obviamente en función de las dependencias y para maximizar la eficiencia
(por ejemplo primero se intentan ejecutar las que son dependencias comunes a otras tareas)
y finalmente ejecutarlas.

Los tipos de archivos de configuración que maneja [BitBake] son:

<dl>
 <dt>Recetas (.bb)</dt>
 <dd>Contienen información acerca de un componente de software concreto. Entre
 dicha información, por ejemplo, podemos destacar: desde donde descargar los
 parches para las fuentes, que configuraciones deben ser aplicadas antes de
 la compilación, como se compila el componente y como se empaqueta el resultado.</dd>
 <dt>Clases (.bbclass)</dt>
 <dd>Contienen información que es interesante compartir entre distintas recetas.
 Por ejemplo la clase **autotools**, que contiene configuraciones comunes para
 cualquier aplicación que utiliza la herramienta **autotools**.</dd>
 <dt>Configuraciones (.conf)</dt>
 <dd>Define diversas variables de configuración que controlan lo que Poky va
 a hacer. Esto incluye configuraciones específicas de la maquina, opciones de
 configuración de la distribución, ajustes del compilador, configuraciones de
 usuario, etc.</dd>
</dl>

[BitBake] puede combinar varios de estos archivos en los se denomina como **capas**.
Una capa es un agrupamiento de recetas que proporciona algún tipo de funcionalidad
adicional. Pueden ser un [BSP] para un nuevo dispositivo, tipos de imágenes
adicionales o software no incluido en Poky.

Los mismos metadatos principales del proyecto [Yocto], **meta-yocto**, son por si
mismos una capa aplicada sobre la capa de metadatos OE-Core que añade software
adicional y tipos de imágenes a esta última.

Un ejemplo de como funciona esto se puede ver al crear un dispositivo [NAS]
(Network-attached Storage) para la CPU Intel E660
([Crown Bay](http://www.intel.com/p/es_XL/embedded/hwsw/hardware/atom-e6xx/overview))
usando x32, el nuevo [ABI] nativo de 32 bits para procesadores x86-64:
    
 1. En el nivel más bajo colocaríamos una capa [BSP] para Crown Bay que activaría
 funcionalidades específicas del hardware de estos procesadores.
 Esta capa, por ejemplo, incluiría los drivers de vídeo.
 2. Como queremos utilizar x32, añadiríamos posteriormente la capa **meta-x32**.
 3. La funcionalidad de [NAS] se incorporaría añadiendo la capa **meta-bayron**,
 que el mismo proyecto [Yocto] nos ofrece como ejemplo.
 4. Finalmente incorporaríamos una capa, que imaginariamente llamaremos
 **meta-myproject**, para proveer el software y la configuraciones necesarias
 para crear una interfaz gráfica de usuario de configuración del [NAS].

Como hemos comentado, cada una de estas capas estaría formada por uno o más
archivos de configuración de los tipos indicados anteriormente.

## Referencias

 1. [The Yocto Proyect](http://www.aosabook.org/en/yocto.html).
 [The Architecture of Open Source Applications](http://www.aosabook.org/).
 2. [Yocto Proyect FAQ](https://wiki.yoctoproject.org/wiki/FAQ).
 3. [Poky HandBook](http://www.yoctoproject.org/docs/1.0/poky-ref-manual/poky-ref-manual.html)

[Yocto]: https://www.yoctoproject.org/ "Yocto Project"
[Poky]: http://www.pokylinux.org/ "Poky Plataform Builder"
[BitBake]: http://en.wikipedia.org/wiki/BitBake "BitBake"
[QEMU]: http://wiki.qemu.org/ "QEMU"
[OpenEmbedded]: http://www.openembedded.org/ "OpenEmbedded"
[Eclipse]: http://www.eclipse.org/ "Eclipse IDE"
[NAS]: http://es.wikipedia.org/wiki/Network-attached_storage "Network-attached storage"
[ABI]: http://en.wikipedia.org/wiki/Application_binary_interface "Application binary interface"
[BSP]: http://en.wikipedia.org/wiki/Board_support_package "Board Support Package"