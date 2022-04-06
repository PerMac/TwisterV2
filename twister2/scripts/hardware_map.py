import logging
import platform
import re
from pathlib import Path

import yaml
from serial.tools import list_ports
from twister2.device.hardware_map import HardwareMap

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

MANUFACTURER = [
    'ARM',
    'SEGGER',
    'MBED',
    'STMicroelectronics',
    'Atmel Corp.',
    'Texas Instruments',
    'Silicon Labs',
    'NXP Semiconductors',
    'Microchip Technology Inc.',
    'FTDI',
    'Digilent'
]

RUNNER_MAPPING = {
    'pyocd': [
        'DAPLink CMSIS-DAP',
        'MBED CMSIS-DAP'
    ],
    'jlink': [
        'J-Link',
        'J-Link OB'
    ],
    'openocd': [
        'STM32 STLink', '^XDS110.*', 'STLINK-V3'
    ],
    'dediprog': [
        'TTL232R-3V3',
        'MCP2200 USB Serial Port Emulator'
    ]
}


def scan(persistent: bool = False, filename: str = None) -> int:
    """Scan for connected devices and generate hardware map."""
    hardware_map_list = []
    if persistent and platform.system() == 'Linux':

        by_id = Path('/dev/serial/by-id')

        def readlink(link):
            return str((by_id / link).resolve())

        persistent_map = {
            readlink(link): str(link)
            for link in by_id.iterdir()
        }
    else:
        persistent_map = {}

    serial_devices = list_ports.comports()
    logger.info('Scanning connected hardware...')

    for device in serial_devices:
        logger.info('Found device: %s', device)
        if device.manufacturer in MANUFACTURER:

            # TI XDS110 can have multiple serial devices for a single board
            # assume endpoint 0 is the serial, skip all others
            if device.manufacturer == 'Texas Instruments' and not device.location.endswith('0'):
                continue
            hardware_map = HardwareMap(
                platform='unknown',
                id=device.serial_number,
                serial=persistent_map.get(device.device, device.device),
                product=device.product,
                runner='unknown',
                connected=True
            )

            for runner in RUNNER_MAPPING.keys():
                products = RUNNER_MAPPING.get(runner)
                if device.product in products:
                    hardware_map.runner = runner
                    continue
                # Try regex matching
                for product in products:
                    if re.match(product, device.product):
                        hardware_map.runner = runner

            hardware_map.connected = True
            hardware_map.lock = None
            hardware_map_list.append(hardware_map)
        else:
            logger.warning('Unsupported device (%s): %s' % (device.manufacturer, device))

        if filename:
            with open(filename, 'w', encoding='UTF-8') as file:
                hardware_map_list_2 = [device.asdict() for device in hardware_map_list]
                yaml.dump(hardware_map_list_2, file, Dumper=yaml.Dumper, default_flow_style=False)
                logger.info('Saved as %s', filename)
        else:
            import pprint
            pprint.pprint(hardware_map_list)
        return 0
