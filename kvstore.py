import os
import sys

DB_FILE = os.path.join(os.path.dirname(__file__), "data.db")

class KVStore:
    def __init__(self):
        self.keys = []     # In-memory key list
        self.values = []   # In-memory value list
        self.load_from_disk()

    def load_from_disk(self):
        """Replay the append-only log to rebuild the in-memory store."""
        if not os.path.exists(DB_FILE):
            return
        with open(DB_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(" ", 2)
                if len(parts) == 3 and parts[0] == "SET":
                    key, value = parts[1], parts[2]
                    self.set_key(key, value, write_to_file=False)

    def set_key(self, key, value, write_to_file=True):
        """Set the value for a key."""
        if key in self.keys:
            index = self.keys.index(key)
            self.values[index] = value
        else:
            self.keys.append(key)
            self.values.append(value)

        if write_to_file:
            with open(DB_FILE, "a") as f:
                f.write(f"SET {key} {value}\n")
                f.flush()
                os.fsync(f.fileno())

    def get_key(self, key):
        """Retrieve a key's value, or empty string if not found."""
        if key in self.keys:
            index = self.keys.index(key)
            return self.values[index]
        return ""

def main():
    store = KVStore()
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            parts = line.split(" ", 2)
            command = parts[0].upper()

            if command == "SET" and len(parts) == 3:
                store.set_key(parts[1], parts[2])
            elif command == "GET" and len(parts) == 2:
                print(store.get_key(parts[1]), flush=True)
            elif command == "EXIT":
                break
            else:
                print("Invalid command", flush=True)
    except EOFError:
        pass

if __name__ == "__main__":
    main()
