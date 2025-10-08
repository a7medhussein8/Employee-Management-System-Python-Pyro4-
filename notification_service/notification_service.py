import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class NotificationService:
    def __init__(self):
        # Also mirror to DatabaseService for persistence
        self.db = Pyro4.Proxy("PYRONAME:DatabaseService")
        self._buffer = []  # in-memory buffer for quick reads

    def send_message(self, message: str):
        self._buffer.append(message)
        self.db.append_notification(message)
        return "ok"

    def recent(self, limit: int = 20):
        return self._buffer[-limit:]

    def all_from_db(self):
        return self.db.list_notifications()

def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(NotificationService)
    ns.register("NotificationService", uri)
    print("[NotificationService] Ready.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
