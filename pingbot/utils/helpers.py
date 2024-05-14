import os
import signal
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

import asyncio
from multiprocessing import Process
from pingbot.resources.models import PingBot
from pingbot.utils.blockchain import listen_to_event
from pingbot.utils import logger

class PingProcessStarter:
    """ PingBot Multi Process"""

    def __init__(self):
        self.ping = PingBot.objects.get(pk=1)

    def start_event_loop(self, amm_pool):
        asyncio.run(listen_to_event(amm_pool))

    def run(self):
        can_start_up = self.ping.mint_pair != None and int(self.ping.pid) != 0 and self.ping.paused == False
        first_time_start = self.ping.mint_pair != None  and int(self.ping.pid) == 0 and self.ping.paused == False
        amm_id = self.ping.mint_pair
        print(can_start_up, first_time_start)
        # was stopped before by false
        if can_start_up:
            _process = Process(target=self.start_event_loop, args=(amm_id,))
            _process.start()
            self.ping.pid = _process.pid
            self.ping.save()
        elif first_time_start:
            logger.info("First Time Starter")
            _process = Process(target=self.start_event_loop, args=(amm_id,))
            _process.start()
            self.ping.pid = _process.pid
            self.ping.save()


    def stop(self):
        try:
            pid = self.ping.pid
            os.kill(pid,signal.SIGTERM)
            self.ping.pid = 0
            self.ping.save()
        except ProcessLookupError:
                logger.error(f"No process with PID {pid} found.")
        except Exception as e:
                logger.error(f"Error stopping the process: {e}")
