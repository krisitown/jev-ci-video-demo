import sqlite3


class SqliteLabelStore:
    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute("""CREATE TABLE item_labels (
            item_id TEXT, position INTEGER, label TEXT,
            PRIMARY KEY (item_id, position))""")

    def labels(self, item_id):
        return [row[0] for row in self.db.execute(
            "SELECT label FROM item_labels WHERE item_id = ? ORDER BY position",
            (item_id,),
        )]

    def replace_labels(self, item_id, labels):
        self.delete_labels(item_id)
        for position, label in enumerate(labels):
            self.insert_label(item_id, position, label)
        self.flush()

    def delete_labels(self, item_id):
        self.db.execute("DELETE FROM item_labels WHERE item_id = ?", (item_id,))

    def insert_label(self, item_id, position, label):
        self.db.execute("INSERT INTO item_labels VALUES (?, ?, ?)",
                        (item_id, position, label))

    def flush(self):
        self.db.commit()
