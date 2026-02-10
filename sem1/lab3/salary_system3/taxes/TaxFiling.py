from .TaxAuthority import TaxAuthority


class TaxFiling:
    def __init__(
        self,
        filing_id: str,
        period: str,
        status: str,
        tax_authority: "TaxAuthority"
    ):
        self.filing_id: str = filing_id
        self.period: str = period
        self.status: str = status
        self.tax_authority: TaxAuthority = tax_authority

    def prepare(self) -> bool:
        return True

    def submit(self) -> bool:
        self.status = "submitted"
        return True

    def validate_before_submit(self) -> bool:
        if self.status not in ("prepared", "ready"):
            return False
        if not self.period or not isinstance(self.period, str):
            return False
        if not self.tax_authority or not hasattr(self.tax_authority, "validate_taxpayer"):
            return False
        return True
