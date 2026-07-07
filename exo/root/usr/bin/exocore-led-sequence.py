#!/usr/bin/env python3
import time
import os

# Solar Sequence Pinleri (Örn: Merkür, Venüs, Dünya, Mars)
LED_PINS = ["17", "27", "22", "23"]

def setup():
    for pin in LED_PINS:
        if not os.path.exists(f"/sys/class/gpio/gpio{pin}"):
            with open("/sys/class/gpio/export", "w") as f:
                f.write(pin)
        with open(f"/sys/class/gpio/gpio{pin}/direction", "w") as f:
            f.write("out")

def sequence():
    # Arpej ile senkronize 4 aşamalı geçiş
    for pin in LED_PINS:
        with open(f"/sys/class/gpio/gpio{pin}/value", "w") as f:
            f.write("1")
        time.sleep(0.15) # Arpej notasının hızıyla eşleşme
    
    time.sleep(1) # Tüm gezegenler yandıktan sonra bekleme
    
    # Ready durumu (hepsi 3 kez yanıp söner)
    for _ in range(3):
        for pin in LED_PINS:
            with open(f"/sys/class/gpio/gpio{pin}/value", "w") as f: f.write("0")
        time.sleep(0.2)
        for pin in LED_PINS:
            with open(f"/sys/class/gpio/gpio{pin}/value", "w") as f: f.write("1")
        time.sleep(0.2)

if __name__ == "__main__":
    try:
        setup()
        sequence()
    except Exception:
        pass