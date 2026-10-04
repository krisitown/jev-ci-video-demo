from src.ports import LabelStore


class LabelService:
    def __init__(self, store: LabelStore):
        self.store = store

    def labels_for(self, item_id: str) -> list[str]:
        return self.store.labels(item_id)

    def set_labels(self, item_id: str, labels: list[str]) -> None:
        self.store.delete_labels(item_id)
        for position, label in enumerate(labels):
            self.store.insert_label(item_id, position, label)
        self.store.flush()
