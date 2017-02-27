-------------------------------
Preparación raspberry
-------------------------------

1) Se graba la imagen del "Raspbian Jessie Lite" a la SD

2) Editamos el fichero config.txt (equivalente a la BIOS en Raspberry) y añadimos la siguiente línea:

```
dtoverlay=pi3-disable-bt
```

>De esta manera se desactiva el bluetooth y queda habilitado el puerto serial UART (GND, 14 AMARILLO y 15 NARANJA del cable de RS electronica USB-UART)

http://www.ftdichip.com/FTDrivers.htm

3) Nos conectamos por Serie en el putty: COMX (según puerto serie del USB) y 115200 bps, así ya funciona correctamente por serie (GND=negro, GPIO14=amarillo, GPIO15=Naranja)

4) Editamos ficheros /etc/hostname y /etc/hosts con el hostname correspondiente a esta raspberry. Se hace la reserva por DHCP en el router para que se le asigne automáticamente la IP.

5) Se configura el wifi si es necesario, de la siguiente manera:

	Comando: "wpa_passphrase ICPG ICPG123456 >> /etc/wpa_supplicant/wpa_supplicant.conf" (Network_name, Password) 

6) Reiniciamos raspberry y se conectarán las interfaces de red automáticamente


----------------------------------
Configuración raspberry barreras
----------------------------------

1) Conectamos a la raspberry por SSH (o cable serial)

2) `sudo su && cd`

3) `apt-get install python3 python3-pip`

4) `pip3 install virtualenv`

5) `virtualenv pgmenv` __(crear entorno virtual)__

6) copiar código de la aplicación a `/home/pi/`

7) `ln -s /home/pi/barrier-client-rasp /root/barrier-client-rasp`

8) `cd /root && ./pgmenv/bin/activate`

9) `cd /root/barrier-client-rasp && pip3 install -r requirements.txt`

10) `mkdir /var/pgm` es la localización del fichero de base de datos

-------------------------------------------------
Arranque automático raspberry barreras al reboot
-------------------------------------------------

1) creamos un script en /etc/init.d/raspserver

```
case $1 in
        start)
                if [ $(ps -fe | grep python | grep -v grep | wc -l) -eq 0 ] ;then
                    cd /root/barrier-client-rasp && /root/pgmenv/bin/python app.py &
                else
                    echo "Raspberry server is already running..."
                fi
        ;;
        stop)
                pkill -9 python
        ;;
        *)
                echo "Usage: $0 (start|stop)"
        ;;
esac
```
2) En el fichero `/etc/rc.local` antes del exit 0, hay que añadir la siguiente línea:

`/etc/init.d/raspserver start`

3) Dar permisos de ejecución el fichero creado en el primer punto de este apartado

`chmod 755 /etc/init.d/raspserver`
