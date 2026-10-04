from src.ports import LabelStore


class LabelService:
    def __init__(self, store: LabelStore):
        self.store = store

    def labels_for(self, item_id: str) -> list[str]:
        return self.store.labels(item_id)

    def set_labels(self, item_id: str, labels: list[str]) -> None:
        self.store.replace_labels(item_id, labels)
