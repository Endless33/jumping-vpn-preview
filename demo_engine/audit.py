class Audit:
    def check_identity_reset(self, old_id: str, new_id: str) -> bool:
        return old_id == new_id

    def check_dual_binding(self, active: list) -> bool:
        return len(active) <= 1