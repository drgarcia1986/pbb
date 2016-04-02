

class NotificationBackend:

    def _pre_notify(self, message):
        pass

    def _post_notify(self, message):
        pass

    def _notify(self, message):
        raise NotImplementedError

    def notify(self, message):
        self._pre_notify(message)

        result = self._notify(message)

        self._post_notify(message)

        return result
