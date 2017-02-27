#!/usr/bin/env python

import pigpioext


class Decoder:
    """
    A class to read Wiegand codes of an arbitrary length.

    The code length and value are returned.

    EXAMPLE

    #!/usr/bin/env python

    import time

    import pigpioext

    import wiegandext

    def callback(bits, code):
       if (bits > 25):
           print("bits={} code={}".format(bits, code))

    pi = pigpio.pi()

    w = wiegandext.decoder(pi, 14, 15, callback)

    time.sleep(300)

    w.cancel()

    pi.stop()
    """

    def __init__(self, pi, gpio_0, gpio_1, callback, bit_timeout=5):

        """
        Instantiate with the pi, gpio for 0 (green wire), the gpio for 1
        (white wire), the callback function, and the bit timeout in
        milliseconds which indicates the end of a code.

        The callback is passed the code length in bits and the value.
        """

        self.pi = pi
        self.gpio_0 = gpio_0
        self.gpio_1 = gpio_1

        self.callback = callback

        self.bit_timeout = bit_timeout

        self.in_code = False

        self.pi.set_mode(gpio_0, pigpioext.INPUT)
        self.pi.set_mode(gpio_1, pigpioext.INPUT)

        self.pi.set_pull_up_down(gpio_0, pigpioext.PUD_UP)
        self.pi.set_pull_up_down(gpio_1, pigpioext.PUD_UP)

        self.cb_0 = self.pi.callback(gpio_0, pigpioext.FALLING_EDGE, self._cb)
        self.cb_1 = self.pi.callback(gpio_1, pigpioext.FALLING_EDGE, self._cb)

    def _cb(self, gpio, level, tick):

        """
        Accumulate bits until both gpios 0 and 1 timeout.
        """

        if level < pigpioext.TIMEOUT:

            if self.in_code is False:
                self.bits = 1
                self.num = 0
                self.in_code = True
                self.code_timeout = 0
                self.pi.set_watchdog(self.gpio_0, self.bit_timeout)
                self.pi.set_watchdog(self.gpio_1, self.bit_timeout)
            else:
                self.bits += 1
                self.num <<= 1

            if gpio == self.gpio_0:
                self.code_timeout &= 2  # clear gpio 0 timeout
            else:
                self.code_timeout &= 1  # clear gpio 1 timeout
                self.num |= 1

        else:

            if self.in_code:

                if gpio == self.gpio_0:
                    self.code_timeout |= 1  # timeout gpio 0
                else:
                    self.code_timeout |= 2  # timeout gpio 1

                if self.code_timeout == 3:  # both gpios timed out
                    self.pi.set_watchdog(self.gpio_0, 0)
                    self.pi.set_watchdog(self.gpio_1, 0)
                    self.in_code = False
                    self.callback(self.bits, self.num)

    def cancel(self):

        """
        Cancel the Wiegand decoder.
        """

        self.cb_0.cancel()
        self.cb_1.cancel()


if __name__ == "__main__":
    import time

    import pigpioext

    import wiegandext


    def callback(bits, value):
        print("number of bits: %d" % bits)
        print("value: {}".format(value))
        binari = bin(value)
        print("binary: %s" % binari)
        hexadecimal = hex(value >> 1)
        hexa_int = int(hexadecimal, 16)
        final_hex = ("%x" % hexa_int)
        if len(final_hex) > 8:
            final_hex = final_hex[1:]
        print("bits=%d value=%d hex=%x correct_hex=%s" % (bits, value, hexa_int, final_hex))


    pi = pigpioext.pi()

    w = wiegandext.Decoder(pi, 20, 21, callback)

    time.sleep(1000)

    w.cancel()

    pi.stop()
