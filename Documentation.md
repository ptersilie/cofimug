# Documentation

As the COMEN Wifi Smart Plugs don't provide any documentation I will try to document here what I was able
to find out through reverse engineering of the app.

## Message format

Messages sent to the devices are in a bytecode format consisting of multiple parts.
The following example shows a message send by the app:

```
             Length of encrypted message
                        \/
01 40 AA BB CC DD EE FF 10 4f ae e1 e5 fb 67 dc 28 07 0d 43 44 e5 43 26 5f
      \      MAC      /    \              Encrypted message              /
```

The first 9 bytes contain the MAC address of the device and some other stuff.
Let's go through them byte-by-byte:

```
Byte   1: 01                - Beginning of the bytecode. Seems to be fixed.
Byte   2: 40                - Some boolean. Reason unclear.
Byte 3-8: AA BB CC DD EE FF - MAC address of the device we want to talk to
Byte   9: 10                - Length of the remaining, encrypted message
Byte 9-X: ...               - Encrypted message
```

Onto the encrypted part of the message (starting at byte 9). Once we decrypt it
we receive this:

```
00 01 4E C2 11 92 DD 01 00 00 00 FF
```

And here’s the explanation:

```
Byte    1: 00             - Beginning of the bytecode. Seems to be fixed.
Byte  2-3: 01 4E          - Counter that is increased with every message.
                            Presumably used to sort the order of the UDP messages. Leaving this 0 works well
                            enough in a local network. However, since UDP gives no guarantee about the order of
                            arrival of packages this might be useful to remember when things don't work properly.
Byte    4: D3             - Company code
Byte    5: 13             - Device type
Byte  6-7: 81 CC          - Auth code
Byte 8-12: 01 00 00 00 FF - The message. Switch on: 01 00 00 FF FF. Switch off: 01 00 00 00 FF.
```

Company code, device type, and auth code are needed to identify the device. If
incorrect the device will ignore the message. The values can be retrieved by
either listening to port `8530` when sending commands over the app and
decrypting the messages, or through the distributors website (see ReadMe).

## Encryption

To encrypt and decrypt the messages we can use any AES implementation, using the following values:

- Algorithm: AES/CBC/PKCS5PADDING
- IVParameter: 123456789abcdef
- Secret Key: 123456789abcdef

## Additional notes

- If a command the device has been successful, it will reply with the same
  message on the same port (except byte 8 of the decrypted message changes from
  `01` to `06`). For instance if the device is turned off and a message is sent
  to turn it on, it will reply with the on message. If the device was already
  off it won’t reply at all. It also won’t reply if it couldn’t understand the
  message.
