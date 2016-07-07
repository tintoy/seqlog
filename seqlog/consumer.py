from queue import Queue, Empty
from threading import Thread


class LogRecordConsumer:
    """
    Consumes log records from a queue.
    """

    def __init__(self, queue, callback, batch_size):
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
        """

        self.consumer_thread = None
        self.current_batch = []
        self.is_running = False

        self.queue = queue
        self.callback = callback
        self.batch_size = batch_size

    def start(self):
        """
        Start the consumer.
        """

        if self.is_running:
            raise Exception("The consumer is already running.")

        self.consumer_thread = Thread(
            name="Seq log entry consumer",
            target=self._process_queue,
            daemon=True
        )
        self.is_running = True
        self.consumer_thread.start()

    def stop(self):
        """
        Stop the consumer.
        """

        if not self.is_running:
            raise Exception("The consumer is not running.")

        self.is_running = False
        self.consumer_thread = None

    def _process_queue(self):
        """
        Process the record queue.
        """

        while self.is_running:
            try:
                record = self.queue.get(block=True, timeout=500)
            except Empty:
                pass
            else:
                self.current_batch.append(record)
                if len(self.current_batch) < self.batch_size:
                    continue

                current_batch = self.current_batch[:]
                self.current_batch.clear()

                self.callback(current_batch)
