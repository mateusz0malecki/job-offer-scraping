from fastapi import HTTPException, status


class OfferNotFound(HTTPException):
    def __init__(self, offer_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job offer with id '{offer_id}' not found."
        )
