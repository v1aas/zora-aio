class Contract:
    def __init__(
            self,
            name: str,
            contract: str,
            contract_type: str,
            max_supply: int,
            total_mints: int,
            is_reported: bool,
            mint_choices: dict = None,
            token_id: list = None
    ):
        self.name = name
        self.contract = contract
        self.contract_type = contract_type
        self.max_supply = max_supply
        self.total_mints = total_mints
        self.is_reported = is_reported
        self._mint_choices = mint_choices
        self.token_id = token_id
    
    @property
    def mint_choices(self):
        return self._mint_choices

    @mint_choices.setter
    def mint_choices(self, value):
        self._mint_choices = value

    def __str__(self):
        return (
            f"name: {self.name} \n"
            f"contract: {self.contract} \n"
            f"contract_type: {self.contract_type} \n"
            f"max_supply: {self.max_supply} \n"
            f"total_mints: {self.total_mints} \n" 
            f"is_reported: {self.is_reported} \n"
            f"mint_choices: {self._mint_choices} \n"
            f"token_id: {self.token_id}"
            )
