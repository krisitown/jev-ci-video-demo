from src.ports import LabelStore


class LabelService:
    def __init__(self, store: LabelStore):
        self.store = store

    def labels_for(self, item_id: str) -> list[str]:
        return self.store.labels(item_id)
