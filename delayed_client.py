import logging
import random
import time

from instagrapi import Client

logger = logging.getLogger(__name__)

class DelayedClient(Client):
    """Instagram Client that waits a random time before each request."""

    def __init__(self, min_delay: float = 2.0, max_delay: float = 7.0, jitter: float = 0.5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.jitter = jitter

    def _sleep_before_request(self) -> None:
        delay = random.uniform(self.min_delay, self.max_delay)
        if self.jitter:
            delay += random.uniform(-self.jitter, self.jitter)
        delay = max(0.0, delay)
        logger.debug("Delay before request: %.2f seconds", delay)
        time.sleep(delay)

    def private_request(self, *args, **kwargs):
        self._sleep_before_request()
        return super().private_request(*args, **kwargs)

    def public_request(self, *args, **kwargs):
        self._sleep_before_request()
        return super().public_request(*args, **kwargs)
