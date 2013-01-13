Title: Raspberry Pi
Tags: rpi, raspberry pi, arm, gpio, videocore, broadcom
Date: 2013-01-13

Una Raspberry Pi es una placa computadora ([SBC]) de bajo coste que incluye:

<img src="http://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/RaspberryPi.jpg/320px-RaspberryPi.jpg" style="float:right;margin:0 0px 10px 0">

 * Un [SOC] Broadcom BCM2835, que contiene una CPU [ARM11]76JZF-S a 700 MHz y
una GPU [VideoCore] IV.
 * 512 MB de memoria RAM (en la versión B de Raspberry Pi, 256 MB en la versión A)
instalada sobre la CPU.
 * Una ranura de tarjetas SD/MMC/SDIO para el almacenamiento no volatil.
 * 1 puerto Ethernet de 10/100Mb.
 * 2 puertos USB 2.0.
 * 1 puerto micro USB de alimentación.
 * 1 puerto tipo A de salida HDMI 1.3.a
 * 1 conector RCA de salida de video compuesto.
 * 1 conector jack esterio de 3.5mm para la salida de audio.
 * 1 conector de expansión de 26 pines con:
    * 8 puertos [GPIO] a 3.3v.
    * 2 puertos seriales ([UART]) a 3.3v TTL o 2 puertos [GPIO] a 3.3v.
    * 1 interfaz [I2C] (3.3v) o 2 puertos [GPIO] a 3.3v.
    * 1 interfaz [SPI] (3.3v) o 5 puertos [GPIO] a 3.3v.
    * Diversos pines a 3.3v, 5v y tierra (GND).

entre otros componentes. En la web del proyecto colaborativo [Raspberry Pi Wiki]
hay disponible más información sobre todo este [hardware].
    
Respecto al software la [Fundación Raspberry Pi] da soporte para las distribuciones
[Raspbian] (derivada de Debian), [RISC OS](http://es.wikipedia.org/wiki/RISC_OS)
y Arch Linux y promueve principalmente el aprendizaje de los lenguajes de
programación [Python] y [Scratch] con [fines educativos](http://www.raspberrypi.org/archives/2965).

Otra organización que se ha volcado en Raspberry Pi es [Adafruit]. Esta compañía
en la actualidad provee [productos](https://www.adafruit.com/raspberrypi) relacionados,
[formación](http://learn.adafruit.com/category/raspberry-pi), su propia
distribución [Adafruit Raspberry Pi Educational Linux Distro](http://learn.adafruit.com/adafruit-raspberry-pi-educational-linux-distro),
que tiene algunas ventajas respecto a las oficiales, y el
entorno de desarrollo [Raspberry Pi WebIDE](http://learn.adafruit.com/webide/)
basado en web para crear facilmente aplicaciones en [Python], Ruby o JavaScript.

## Referencias adicionales

 1. [Raspberry Pi Educational Manual](http://downloads.raspberrypi.org/Raspberry_Pi_Education_Manual.pdf).
 1. [RPi Hardware] en [Raspberry Pi Wiki].
 1. [RPi Low-level periperals](http://elinux.org/RPi_Low-level_peripherals) en [Raspberry Pi Wiki] (incluye el detalle del conector de expasión).
 1. [BCM2835 ARM Peripherals](http://www.raspberrypi.org/wp-content/uploads/2012/02/BCM2835-ARM-Peripherals.pdf).
 1. [ARM1176JZF-S Technical Reference Manual](http://infocenter.arm.com/help/topic/com.arm.doc.ddi0301h/DDI0301H_arm1176jzfs_r0p7_trm.pdf).
 1. [Raspberry Pi 2.0 Schematics](http://www.raspberrypi.org/wp-content/uploads/2012/10/Raspberry-Pi-R2.0-Schematics-Issue2.2_027.pdf)

[SBC]: http://en.wikipedia.org/wiki/Single-board_computer "Single-board Computer"
[SOC]: http://es.wikipedia.org/wiki/System_on_a_chip "System on a Chip"
[ARM11]: http://en.wikipedia.org/wiki/ARM11 "ARM11"
[VideoCore]: http://en.wikipedia.org/wiki/VideoCore "VideoCore"
[GPIO]: http://en.wikipedia.org/wiki/General_Purpose_Input/Output "General-Purpose Input/Output"
[UART]: http://es.wikipedia.org/wiki/Universal_Asynchronous_Receiver-Transmitter "Universal Asynchronous Receiver-Transmitter"
[I2C]: http://es.wikipedia.org/wiki/I2C "I²C (Inter-Integrated Circuit)"
[SPI]: http://es.wikipedia.org/wiki/SPI "Serial Peripheral Interface"
[hardware]: http://elinux.org/RPi_Hardware "RPi Hardware"
[RPi Hardware]: http://elinux.org/RPi_Hardware "RPi Hardware"
[Raspberry Pi Wiki]: http://elinux.org/RPi_Hub "RPi Hub"
[Fundación Raspberry Pi]: http://www.raspberrypi.org/about "Raspberry Pi Foundation"
[Scratch]: http://es.wikipedia.org/wiki/Scratch_(lenguaje_de_programaci%C3%B3n) "Lenguage de programación Scratch"
[Python]: http://es.wikipedia.org/wiki/Python "Lenguage de programación Python"
[Raspbian]: http://www.raspbian.org/ "Raspbian"
[RISC OS]: http://es.wikipedia.org/wiki/RISC_OS "RISC OS"
[Adafruit]: http://www.adafruit.com/blog/category/raspberry-pi/ "Adafruit - Raspberry Pi"