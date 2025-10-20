import os
import sys

DB_FILE = "data.db"

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

    def get_key(self, key):
        """Get the value for a key."""
        if key in self.keys:
            index = self.keys.index(key)
            return self.values[index]
        else:
            return "key not set"

def main():
    store = KVStore()
    for line in sys.stdin:
        parts = line.strip().split(" ", 2)
        if not parts:
            continue
        command = parts[0].upper()

        if command == "SET" and len(parts) == 3:
            key, value = parts[1], parts[2]
            store.set_key(key, value)
        elif command == "GET" and len(parts) == 2:
            key = parts[1]
            print(store.get_key(key))
        elif command == "EXIT":
            break
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()