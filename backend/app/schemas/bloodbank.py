from pydantic import BaseModel

from app.db.sqlc.bloodbank import GetAllBloodBanksRow


class BloodbankDTO(BaseModel):
    bloodbank_id: int
    name: str
    street_name: str
    street_number: str
    postal_code: str
    city: str
    country: str
    user_has_admin_access: bool

    @staticmethod
    def map_bloodbank(row: GetAllBloodBanksRow) -> BloodbankDTO:
        return BloodbankDTO(
            bloodbank_id=row.bloodbank_id,
            name=row.name,
            street_name=row.street_name,
            street_number=row.street_number,
            postal_code=row.postal_code,
            city=row.city,
            country=row.country,
            user_has_admin_access=row.user_has_admin_access,
        )
