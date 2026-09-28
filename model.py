from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship, Session


# -------------------------
# Artist 資料表
# -------------------------
class Artist(SQLModel, table=True):
    __tablename__ = "artists"

    artist_id: str = Field(primary_key=True)
    artist_name: str
    artist_hotness: float

    songs: List["Song"] = Relationship(back_populates="artist")


# -------------------------
# Song 資料表
# -------------------------
class Song(SQLModel, table=True):
    __tablename__ = "songs"

    song_id: str = Field(primary_key=True)
    song_title: str = Field(index=True)

    artist_id: str = Field(foreign_key="artists.artist_id")

    song_hotness: Optional[float] = Field(default=None)
    year: Optional[int] = Field(default=None)

    artist: Optional["Artist"] = Relationship(back_populates="songs")

    audio_features: Optional["AudioFeatures"] = Relationship(
        back_populates="song",
        sa_relationship_kwargs={"uselist": False},
    )


# -------------------------
# AudioFeatures 資料表
# -------------------------
class AudioFeatures(SQLModel, table=True):
    __tablename__ = "audio_features"

    song_id: str = Field(
        foreign_key="songs.song_id",
        primary_key=True,
    )

    danceability: float
    energy: float
    key: int
    loudness: float
    tempo: float

    song: Optional["Song"] = Relationship(back_populates="audio_features")

# -------------------------
# UserSongPlay 資料表
# -------------------------
class UserSongPlay(SQLModel, table=True):
    __tablename__ = "user_song_plays"

    id: int | None = Field(default=None, primary_key=True)

    user_id: str = Field(index=True)
    song_id: str = Field(index=True)

    play_count: int