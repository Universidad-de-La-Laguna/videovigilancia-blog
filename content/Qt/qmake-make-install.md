Title: Make install con qmake
Tags: qt, make, qmake, INSTALLS, DEFINES
Date: 2013-04-22

Cada entorno de desarrollo y/o lenguaje de programación maneja por sus propios
medios la manera de definir un proyecto de software y el proceso de construcción
del mismo. Sin embargo [make] sigue siendo ámpliamente utilizado para este
propósito, especialmente en los sistemas UNIX y derivados.

# Make

Para usar [make] cada proyecto debe ir acompañado de un fichero `Makefile` donde
se incluyen las reglas para la compilación y enlazado de las librerías y
ejecutables del mismo. Estas reglas fijan que es lo que hay que hacer —que
comandos ejecutar y como hacerlo— para obtener cada producto del proceso de
construcción, así como las dependencias de estos con respecto a otros productos
o a los distintos archivos de código fuente del proyecto. Además se pueden
incluir reglas para automatizar tareas tales como generar la documentación;
instalar o desplegar los programas, las librerías, la documentación y otros
productos generados; o limpiar el proyecto, borrando archivos temporales y
subproductos de la compilación.

Cuando la construcción de un proyecto ha sido automatizada adecuadamente con
`make`, la compilación del mismo se reduce a ejecutar el comando:

~~~~.sh
$ make
~~~~

en el directorio del proyecto. Siendo su instalación igual de sencilla:

~~~~.sh
$ make install
~~~~

Obviamente entornos integrados de desarrollo como Eclise, KDevelop, Code::Blocks
o Visual Studio incorporan sus propias herramientas para automatizar la
compilación de proyectos, que además se integran perfectamente con estos
entornos gráficos. Sin embargo [make] suele estar disponible en cualquier
sistema y puede ser utilizado independientemente de las preferencias de cada
desarrollador acerca del entorno integrado con el que trabajar.

Además [make] es una herramienta que fácilmente puede ser utilizada desde otras
de más alto nivel. Por ejemplo, un sistema de construcción de paquetes como el
que utilizan las distribuciones basadas en Debian automatiza todos los pasos,
desde la descarga del código fuente hasta la generación del archivo `.deb`,
pasando por invocar a `make` para compilar y a `make install` para que los
productos de dicha construcción se instalen en su ubicación definitiva[^1], de
donde son tomados para conformar el contenido del paquete del proyecto. De forma
muy similar funciona [Bitbake], la herramienta de construcción que utiliza el
proyecto [Yocto] para generar distribuciones de Linux para sistemas empotrados,
y así una larga lista de herramientas similares. Para todas ellas el poder
automatizar la construcción de proyectos de software es fundamental, siendo éste
un campo donde la solución orientada a línea de comandos de [make] se muestra
mucho más flexible que las soluciones de interfaz gráfica integradas de los 
distintos entornos de desarrollo.

# Qmake

Aunque [make] es una herramienta muy flexible, resulta muy compleja de utilizar,
si no imposible, cuando se quiere crear software portable. Diferentes sistemas
operativos pueden tener distintos compiladores, ya sean de diferentes
fabricantes o en distintas versiones, u ofrecer a las aplicaciones diferentes
funcionalidades —o las mismas pero de manera distintas—. Además un proyecto de
software puede depender de otras librerías o programas, que nuevamente pueden
ser de versiones diferentes o distintos desarrolladores. Y a todo eso hay que
unir que según el sistema operativo la ubicación de librerías, programas y
herramientas de desarrollo puede diferir.

Enfrentar estas situaciones con [make] es extremadamente difícil, por lo que los
desarrolladores suelen utilizar otras utilidades que se encarguen de buscar las
herramientas de desarrollo y las dependencias del programa, detectar las
funcionalidades del sistema y generar un archivo `Makefile` ajustado al sistema
concreto donde se va a compilar.

Herramientas de este tipo existen muchas. Por ejemplo Autotools[^2], CMake,
SCons y [qmake]. Siendo esta última la que se usa preferentemente con las
aplicaciones desarrolladas en [Qt], ya que sabe manejar perfectamente las
singularidades de este _framework_.

Con [qmake] las información requerida para construir un proyecto se define en un
[archivo de proyecto] que generalmente tienen extensión `.pro`. Al ejecutar
`qmake` dentro del directorio de un proyecto, éste interpreta los archivos de
proyecto y genera el `Makefile` correspondiente. Después sólo es necesario
ejecutar el comando `make` para iniciar la compilación del mismo:

~~~~.sh
$ qmake
$ make
$ make install
~~~~

# Reglas para make install

Realmente el último `make install` no sirve de mucho porque [qmake] por defecto
no añade tareas a dicha regla en el archivo `Makefile`.

Si queremos que al ejecutar `make install` se instalen los archivos de nuestra
aplicación en las ubicaciones adecuadas[^3], debemos instruir a [qmake] a través
del [archivo de proyecto] acerca de como se hace:

~~~~
unix {          # Esta configuración específica de Linux y UNIX
    # Variables
    #
    isEmpty(PREFIX) {
        PREFIX = /usr/local
    }
    BINDIR  = $$PREFIX/bin
    DATADIR = $$PREFIX/share
    CONFDIR = /etc
    isEmpty(VARDIR) {
        VARDIR  = /var/lib/$${TARGET}
    }

    # Install
    #
    INSTALLS += target config desktop icon32 vardir

    ## Instalar ejecutable
    target.path = $$BINDIR

    ## Instalar archivo de configuración
    config.path = $$CONFDIR
    config.files += $${TARGET}.ini

    ## Instalar acceso directo en el menú del escritorio
    desktop.path = $$DATADIR/applications
    desktop.files += $${TARGET}.desktop

    ## Instalar icono de aplicación
    icon32.path = $$DATADIR/icons/hicolor/32x32/apps
    icon32.files += ./data/32x32/$${TARGET}.png

    ## Crear directorio de archivos variables
    vardir.path = $$VARDIR
    vardir.commands = true
}
~~~~

La variable `INSTALLS` debe contener una lista de los recursos que queremos que
sean instalados con `make install`. De tal forma que cada elemento de la lista
incorpora atributos que proporcionan información sobre dónde van a ser
instalados.

Por ejemplo, el elemento `target` representa a los ficheros resultado de la
construcción del proyecto. Asignando una ruta a `target.path` estamos indicando
donde queremos que sean instalados. De forma similar, el elemento `icon32`
representa al icono de la aplicación en el escritorio. Asignando un valor a
`icon32.path` estamos diciendo donde queremos que sea instalado, mientras que el
valor del atributo `icon32.files` indica donde podemos encontrar el archivo o
archivos del icono respecto al directorio del proyecto.

En teoría podemos especificar cualquier ubicación como destino de nuestros
archivos, aunque es muy recomendable seguir el [Filesystem Hierarchy Standard].

![Filesystem Hierarchy Standard](|filename|/images/fhs.png)

# Definición de macros del preprocesador

Las variables que hemos definido dentro del [archivo de proyecto] establecen la
ubicación de los recursos del programa tras su instalación. Sería más complicado
cometer errores si en nuestro código fuente usáramos directamente las rutas tal
y como se definen en el [archivo de proyecto], sin tener que volver a definirlas
en C++. Además eso daría pie a modificar la ruta de los archivos mediante la
redefinición de variables en la línea de comandos de [qmake], sin tener por ello
que modificar el código fuente. Por ejemplo:

~~~~.sh
$ qmake PREFIX=/usr
~~~~

ejecuta [qmake] usando el valor indicado para la variable `PREFIX`.

Para conseguir esto sólo tenemos que utilizar la variable `DEFINES`, que nos
permite listar un conjunto de macros del preprocesador[^4] que queremos que sean
pasadas al compilador.

~~~~
unix {          # Esta configuración específica de Linux y UNIX
    # Variables
    #
    isEmpty(PREFIX) {
        PREFIX = /usr/local
    }
    BINDIR  = $$PREFIX/bin
    DATADIR = $$PREFIX/share
    CONFDIR = /etc
    isEmpty(VARDIR) {
        VARDIR  = /var/lib/$${TARGET}
    }

    DEFINES += APP_DATADIR=\\\"$$DATADIR\\\"
    DEFINES += APP_VARDIR=\\\"$$VARDIR\\\"
    DEFINES += APP_CONFFILE=\\\"$$CONFDIR/$${TARGET}.ini\\\"

    # Install
    #
    INSTALLS += target config desktop icon32 vardir

    ## Instalar ejecutable
    target.path = $$BINDIR

    ## Instalar archivo de configuración
    config.path = $$CONFDIR
    config.files += $${TARGET}.ini

    ## Instalar acceso directo en el menú del escritorio
    desktop.path = $$DATADIR/applications
    desktop.files += $${TARGET}.desktop

    ## Instalar icono de aplicación
    icon32.path = $$DATADIR/icons/hicolor/32x32/apps
    icon32.files += ./data/32x32/$${TARGET}.png

    ## Crear directorio de archivos variables
    vardir.path = $$VARDIR
    vardir.commands = true
}
~~~~

Así, por ejemplo, dentro del código fuente se puede usar la macro `APP_CONFFILE`
con la ruta al archivo de configuración de la aplicación para acceder a él
mediante [QSettings]:

~~~~.cpp
QSettings settings(APP_CONFFILE, QSettings::IniFormat);
~~~~


# Referencias

 1. [qmake Project
Files](http://qt-project.org/doc/qt-5.0/qtdoc/qmake-project-files.html)
 2. Wikipedia - [Filesystem Hierarchy Standard](http://es.wikipedia.org/wiki/Filesystem_Hierarchy_Standard)

[Qt]: |filename|/Overviews/proyecto-qt.md "Proyecto Qt"
[Yocto]: |filename|/Overviews/yocto-poky-y-bitbake.md "Yocto, Poky y BitBake"
[make]: "http://es.wikipedia.org/wiki/Make" "make"
[BitBake]: |filename|/Overviews/yocto-poky-y-bitbake.md "Yocto, Poky y BitBake"
[qmake]: http://en.wikipedia.org/wiki/Qmake "qmake"
[Filesystem Hierarchy Standard]: http://es.wikipedia.org/wiki/Filesystem_Hierarchy_Standard "Filesystem Hierarchy Standard"
[archivo de proyecto]: http://qt-project.org/doc/qt-5.0/qtdoc/qmake-project-files.html "qmake Project Files"
[QSettings]: http://qt-project.org/doc/qt-5.0/qtcore/qsettings.html "QSettings"
[Filesystem Hierarchy Standard]: http://es.wikipedia.org/wiki/Filesystem_Hierarchy_Standard "Filesystem Hierarchy Standard"

[^1]: Durante el proceso de construcción de un paquete `.deb` el proyecto, una
vez compilado, se instala, pero no en la raíz del sistema donde está teniendo
lugar la compilación, sino que se confina el comando `make install` a un
subdirectorio temporal. Así [make] deposita los archivos en sus ubicaciones
predefinidas (p. ej. `/usr/bin`, `/usr/lib`, `/etc`, `/var/lib`, etc.) solo que
relativas a dicho subdirectorio (p .ej. `/ruta/al/subdirectorio/usr/bin`,
`/ruta/al/subdirectorio/etc`, `/ruta/al/subdirectorio/usr/lib`,
`/ruta/al/subdirectorio/var/lib`, etc.). Para obtener el contenido del paquete
sólo hace falta tomar el contenido del subdirectorio temporal, evitando que el
proceso de construcción ensucie el sistema donde se está ejecutando.
[^2]: GNU Autotools es la herramienta que está detrás de tener que ejecutar
`./configure` antes de compilar muchos programas y librerías libres con [make].
[^3]: En los sistemas Linux, UNIX y derivados éstas ubicaciones vienen definidas
por el [Filesystem Hierarchy Standard].
[^4]: Las macros del preprocesador son aquellas que generalmente se definen en
C/C++ mediante la directiva `#define`.