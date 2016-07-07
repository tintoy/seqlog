from queue import Queue, Empty
from threading import Thread, RLock, Timer
from time import sleep


class QueueConsumer:
    """
    Consumes log records from a queue.
    """

    # Pseudo-record used to abort processing of the record queue.
    _stop_processing = object()

    def __init__(self, queue, callback, batch_size, batch_flush_timeout=None):
        """
        Create a new log record consumer.

        The consumer will publish the current batch with it either contains `batch_size` records.
        TODO: Implement `batch_timeout`.

        :param queue: The log record queue to consume.
        :type queue: Queue
        :param callback: The callback that receives batches of log entries.
        :type callback: callable
        :param batch_size: The maximum number of records per batch.
        :type batch_size: int
        :param batch_flush_timeout: An optional timeout (in milliseconds) before each batch is flushed.
        :type batch_flush_timeout: int
        """

        self.is_running = False

        self.consumer_thread = None
        self.flush_thread = None

        self.current_batch = []
        self.batch_lock = RLock()

        self.queue = queue
        self.callback = callback
        self.batch_size = batch_size
        self.batch_flush_timeout = batch_flush_timeout

    def flush_current_batch(self):
        """
        Flush the current batch (if any).
        """

        self.batch_lock.acquire()
        try:
            if not self.is_running:
                return

            current_batch = self.current_batch[:]
            self.current_batch.clear()

            self.callback(current_batch)
        finally:
            self.batch_lock.release()

    def start(self):
        """
        Start the consumer.
        """

        if self.is_running:
            raise Exception("The consumer is already running.")

        self.consumer_thread = Thread(
            name="Seq log entry consumer",
            target=self._queue_processor,
            daemon=True
        )
        self.is_running = True
        self.consumer_thread.start()

        if self.batch_flush_timeout:
            self.flush_thread = Thread(
                name="Seq log entry consumer flush",
                target=self._batch_flusher,
                daemon=True
            )
            self.flush_thread.start()

    def stop(self):
        """
        Stop the consumer.
        """

        if not self.is_running:
            raise Exception("The consumer is not running.")

        # If the processor thread is blocked waiting for a new record, this stop it gracefully.
        self.queue.put(
            QueueConsumer._stop_processing
        )
        self.is_running = False
        self.flush_thread = None
        self.consumer_thread = None

    def _queue_processor(self):
        """
        Process the record queue.
        """

        while self.is_running:
            try:
                record = self.queue.get(block=True)
            except Empty:
                pass
            else:
                if record is QueueConsumer._stop_processing:
                    self.stop()

                    continue

                self.batch_lock.acquire()
                try:
                    self.current_batch.append(record)
                    if len(self.current_batch) >= self.batch_size:
                        self.flush_current_batch()
                finally:
                    self.batch_lock.release()

    def _batch_flusher(self):
        """
        Thread that flushes the current batch after a timeout appears.
        """

        while self.is_running:
            sleep(self.batch_flush_timeout / 1000)

            if not self.is_running:
                return

            self.flush_current_batch()
