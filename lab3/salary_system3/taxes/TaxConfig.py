from .TaxAuthority import TaxAuthority

class TaxConfig:
    def __init__(
        self,
        config_id: str,
        effective_date: str,
        rules: dict,
        tax_authority: "TaxAuthority"
    ):
        self.config_id: str = config_id
        self.effective_date: str = effective_date
        self.rules: dict = rules
        self.tax_authority: TaxAuthority = tax_authority

    def load_for_jurisdiction(self, jurisdiction: str) -> dict:
        return self.rules if self.tax_authority.jurisdiction == jurisdiction else {}

    def validate(self) -> bool:
        return bool(self.rules)
