import pygame as pg


class Task(pg.sprite.Sprite):
    """Execute functions at a later time and optionally loop it

    This is a silly little class meant to make it easy to create
    delayed or looping events without any complicated hooks into
    pygame's clock or event loop.

        # like a delay
        def call_later():
            pass
        task = Task(call_later, 1000)

        # do something 24 times at 1 second intervals
        task = Task(call_later, 1000, 24)

        # do something every 2.5 seconds forever
        task = Task(call_later, 2500, -1)

        # pass arguments
        task = Task(call_later, 1000, args=(1,2,3), kwargs={key: value})

        # chain tasks
        task = Task(call_later, 2500)
        task.chain(Task(something_else))
    """
    def __init__(self, callback, interval=0, loops=1, args=None, kwargs=None):
        assert (callable(callback))
        assert (loops >= -1)
        super(Task, self).__init__()
        self.interval = interval
        self.loops = loops
        self.callback = callback
        self._timer = 0
        self._args = args if args else list()
        self._kwargs = kwargs if kwargs else dict()
        self._loops = loops
        self._chain = list()

    def chain(self, *others):
        """Schedule Task(s) to execute when this one is finished

        If you attempt to chain a task that will never end (loops=-1),
        then ValueError will be raised.

        :param others: Task instances
        :return: None
        """
        if self._loops == -1:
            raise ValueError
        for task in others:
            assert isinstance(task, Task)
            self._chain.append(task)

    def update(self, dt):
        """Update the Task

        The unit of time passed must match the one used in the
        constructor.

        :param dt: Time passed since last update.
        """
        self._timer += dt
        if self._timer >= self.interval:
            self._timer -= self.interval
            self.callback(*self._args, **self._kwargs)
            if not self._loops == -1:
                self._loops -= 1
                if self._loops <= 0:
                    self._execute_chain()
                    self._chain = None
                    self.kill()

    def _execute_chain(self):
        groups = self.groups()
        for task in self._chain:
            task.add(*groups)
