class TaxAuthority:
    def __init__(
        self,
        authority_id: str,
        jurisdiction: str,
        contact: str
    ):
        self.authority_id: str = authority_id
        self.jurisdiction: str = jurisdiction
        self.contact: str = contact

    def get_rates(self, period: str) -> dict:
        return {"standard": 0.2, "reduced": 0.1}

    def file_declaration(self) -> bool:
        return True
