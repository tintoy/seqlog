from queue import Empty
from threading import Thread, RLock, Timer


class QueueConsumer:
    """
    Consumes log records from a queue.
    """

    def __init__(self, name, queue, callback, batch_size, auto_flush_timeout=None):
        """
        Create a new log record consumer.

        The consumer will publish the current batch with it either contains `batch_size` records.
        If `auto_flush_timeout` is not specified, batches will not be published until they are full.

        :param queue: A short descriptive name for the consumer (appears in thread name).
        :type queue: str
        :param queue: The log record queue to consume.
        :type queue: Queue
        :param callback: The callback that receives batches of log entries.
        :type callback: callable
        :param batch_size: The maximum number of records per batch.
        :type batch_size: int
        :param auto_flush_timeout: An optional timeout (in seconds) before each batch is automatically flushed.
        :type auto_flush_timeout: float
        """

        # AF: There should really be a second is_stopping flag
        # to prevent the consumer from reporting that it's stopped when it's not.
        self.is_running = False

        self.state_lock = RLock()
        self.consumer_thread = None
        self.flush_timer = None

        self.current_batch = []

        self.name = name
        self.queue = queue
        self.callback = callback
        self.batch_size = batch_size
        self.auto_flush_timeout = auto_flush_timeout

    @property
    def current_batch_size(self):
        return len(self.current_batch)

    def flush(self):
        """
        Flush the current batch (if any).
        """

        self.state_lock.acquire()
        try:
            if not self.is_running:
                return

            self._cancel_auto_flush()

            current_batch = self.current_batch[:]
            self.current_batch.clear()

            if len(current_batch) == 0:
                return

            self.callback(current_batch)
        finally:
            self.state_lock.release()

    def start(self):
        """
        Start the consumer.
        """

        if self.is_running:
            raise Exception("The consumer is already running.")

        self.consumer_thread = Thread(
            name="Queue consumer ({})".format(self.name),
            target=self._queue_processor,
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

        self._notify_stop_processing()

    def _queue_processor(self):
        """
        Process the record queue.

        """

        while self.is_running:
            try:
                record = self.queue.get(block=True, timeout=0.25)
            except Empty:
                pass
            else:
                try:
                    if not _should_stop_processing(record):
                        self._add_to_current_batch(record)
                    else:
                        self.is_running = False
                finally:
                    self.queue.task_done()

    def _add_to_current_batch(self, record):
        """
        Add a log record to the current batch.

        :param record: The LogRecord.
        """

        self.state_lock.acquire()
        try:
            self.current_batch.append(record)

            if self.current_batch_size == 1:
                self._schedule_auto_flush()
            elif self.current_batch_size >= self.batch_size:
                self.flush()
        finally:
            self.state_lock.release()

    def _notify_stop_processing(self):
        """
        Enqueue the _stop_processing dummy log record to indicate that the consumer should stop processing the queue.
        """

        # If the processor thread is blocked waiting for a new record, this will let it stop gracefully.
        self.queue.put(_stop_processing_queue)

    def _schedule_auto_flush(self):
        """
        Schedule an automatic flush of the current batch.
        """

        if not self.auto_flush_timeout:
            return  # Auto-flush is disabled.

        self.state_lock.acquire()
        try:
            if self.flush_timer:
                return

            self.flush_timer = Timer(self.auto_flush_timeout, self.flush)
            self.flush_timer.daemon = True
            self.flush_timer.start()
        finally:
            self.state_lock.release()

    def _cancel_auto_flush(self):
        """
        Cancel the scheduled automatic flush (if any) for the current batch.
        """

        if not self.auto_flush_timeout:
            return  # Auto-flush is disabled.

        self.state_lock.acquire()
        try:
            if self.flush_timer:
                self.flush_timer.cancel()
                self.flush_timer = None
        finally:
            self.state_lock.release()


def _should_stop_processing(record):
    """
    Determine whether the specified log record indicates that the consumer should stop processing the queue.

    :param record: The LogRecord (or _stop_processing).
    :return: True, if record is _stop_processing; otherwise, False.
    """

    return record is _stop_processing_queue


# Pseudo-record used to abort processing of the record queue.
# This is necessary because it enables us to unblock a consumer thread waiting for an empty queue.
_stop_processing_queue = object()
