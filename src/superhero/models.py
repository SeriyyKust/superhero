from database import Base
from sqlalchemy import CheckConstraint, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from superhero.static import MAX_LENGTH_HERO_NAME


class HeroModel(Base):
    __tablename__ = "heroes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(MAX_LENGTH_HERO_NAME), unique=True, nullable=False
    )
    intelligence: Mapped[int] = mapped_column(Integer, nullable=False)
    strength: Mapped[int] = mapped_column(Integer, nullable=False)
    speed: Mapped[int] = mapped_column(Integer, nullable=False)
    power: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        Index("index_hero_name_hash", "name", postgresql_using="hash"),
        CheckConstraint("intelligence >= 0", name="check_intelligence_positive"),
        CheckConstraint("strength >= 0", name="check_strength_positive"),
        CheckConstraint("speed >= 0", name="check_speed_positive"),
        CheckConstraint("power >= 0", name="check_power_positive"),
    )
