class ContractDTO:
    def __init__(
            self,
            type: str,
            contract: str,
            mint_choices: dict,
            tokens_id: list
    ):
        self.type = type
        self.contract = contract
        self.mint_choices = mint_choices
        self.tokens_id = tokens_id
    
    def __str__(self):
        return (
            f"type: {self.type} \n"
            f"contract: {self.contract} \n"
            f"mint_choices: {self.mint_choices} \n"
            f"tokens_id: {self.tokens_id} \n"
            )
