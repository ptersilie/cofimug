# COFIMUG - COmen wiFI sMart plUG controller

A collection of scripts that allow basic control over COMEN Wifi plugs. These
plugs are distributed by different companies so may have a different branding
than COMEN. For instance in Germany they are distributed by ALDI and branded as
EasyHome Smart2Connect.

As the COMEN Wifi plugs have no official API, the information used in these scripts
were collected by reverse engineering the smart2connect app. Other distributers
may use different codes and keys. Check the [Documentation](Documentation.md) to learn more about the plugs
API which might help you adapting these scripts for other COMEN devices.

## Install

Messages to the Wifi plugs are AES encrypted. To de- and encrypt our messages we need
`pycrypto`. Install it via `pip`.

```
pip install --user pycrypto
```

## Configuration

First you need to gather some data to configure the scripts to be able to send
messages to your smart plug. You’ll need:

- MAC address
- company code
- device code
- auth code

### Method 1

Once you’ve setup your device using the official app, you can gather this
information from their website using the login data you used to log into the app

Note: This process may differ if you bought the device from another distributor.
You can use Method 2 instead.

```
$ python2 fetchinfo.py <youremail> <yourpassword>
{"list":[{"macAddress":"aabbccddeeff","companyCode":"D3","deviceType":"13","authCode":"81CC","deviceName":"Hauptgerät","imageName":"","orderNumber":1,"lastOperation":1476034214883}],"success":true}
```

### Method 2

Alternatively this information can be retrieved by listening to the network
traffic and decrypting everything the app sends to the device. Run `listen.py`
and then turn the plug on and off through the app:

```
$ python2 listen.py
IP: 192.168.0.111
MAC: AA:BB:CC:DD:EE:FF
Company code: D3
Device type: 13
authCode: 81 CC
Message: 01 00 00 FF FF (ON)
```

### Creating the config file

With the obtained information you can now create a `config.py` using the template. Copy the template,

```
cp config.template config.py
```

and complete it with your data.

```
{
    "Main": {
        "ip": "192.168.0.111",
        "mac": "aa:bb:cc:dd:ee:ff",
        "companycode": "D3",
        "devicecode":  "13",
        "authcode": "81CC"
    }
}
```

## Usage

Now you can use the scripts as follows to integrate them into your home
automation system:

```
$ python plug.py Main on

$ python plug.py Main off
```
