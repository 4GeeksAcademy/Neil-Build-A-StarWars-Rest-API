from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }



class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    eye_color: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    hair: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "hair": self.hair,
        }
    
    
    
class Ships(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    color: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    size: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "size": self.size,
        }
    

class planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    color: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    size: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "size": self.size,
        }



class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    characters_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    ships_id: Mapped[int] = mapped_column(ForeignKey("ships.id"))
    planets_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))


    def serialize(self):
        return {
            "id": self.id,
            "characters_id": self.characters_id,
            "ships_id": self.ships_id,
            "planets_id": self.planets_id,
            "user_id": self.user_id,

        }
    




