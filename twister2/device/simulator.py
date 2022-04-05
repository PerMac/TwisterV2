from __future__ import annotations

import logging
import os
import subprocess
import threading
import time
from pathlib import Path

from twister2.device.device_abstract import DeviceAbstract

logger = logging.getLogger(__name__)


class Simulator(DeviceAbstract):

    def connect(self):
        pass

    def disconnect(self):
        pass

    def flash(self, build_dir: str | Path) -> None:
        command = Path(build_dir) / 'zephyr' / 'zephyr.exe'
        self.log_file = Path(build_dir) / 'device.log'
        logger.info('Flashing device')
        logger.info('Flashing command: %s', command)
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=os.environ.copy(),
            )

            t1 = self.save_process_output_to_file(process, self.log_file)
            t2 = self.terminate_process(process, timeout=60)
            t1.start()
            t2.start()
            t1.join()
            t1.join()
        except subprocess.CalledProcessError as e:
            logger.exception('Flashing failed due to error %s', e)
            raise
        else:
            if process.returncode == 0:
                logger.info('Finished flashing %s', build_dir)

    @staticmethod
    def save_process_output_to_file(process: subprocess.Popen, output_file: str | Path) -> threading.Thread:
        """Create Thread which saves a process output to a file."""
        def read():
            logger.debug('Saving process output to file: %s', output_file)
            with process.stdout:
                with open(output_file, 'w', encoding='UTF-8') as file:
                    for line in iter(process.stdout.readline, b''):
                        file.write(line.decode())

        thread = threading.Thread(target=read)
        thread.setDaemon(True)
        return thread

    @staticmethod
    def terminate_process(process: subprocess.Popen, timeout: float) -> threading.Thread:
        """Create Thread which kills a process after given time."""
        def waiting():
            time.sleep(timeout)
            process.kill()

        thread = threading.Thread(target=waiting)
        thread.setDaemon(True)
        return thread
