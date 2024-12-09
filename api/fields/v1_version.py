### v1版本回复格式
from fields.app_fields import MusicMessage, ResponesMessage
from pydantic import BaseModel
from pydantic import BaseModel, Field
from typing import Optional

class V1ResponesMessage(BaseModel):
    song_id:   int |None = Field(default=None, description="The unique identifier for the song")
    song_name: str |None = Field(default=None, description="The name of the song")
    artist:    str |None = Field(default=None, description="The artist of the song")
    lyric:     str |None = Field(default=None, description="The lyrics of the song")
    image:     str |None = Field(default=None, description="URL of the song's cover image")
    result:    str |None = Field(default=None, description="URL to listen to the song")

    conversation_id: str = Field(default=None, description="The ID of the conversation")
    user: str = Field(default=None, description="The user requesting the music")
    code: int = Field(default=200, description="Response code")
    type: int = Field(default=0., description="The genre of the song")
    message: str = Field(default="好的", description="Response message")
    play_list: Optional[list[MusicMessage]] = Field(default=None, description="List of music messages")

    def copy_from_v2_respones(self, respones: ResponesMessage):
        self.conversation_id = respones.conversation_id
        self.user            = respones.user
        self.code            = respones.code
        self.type            = respones.type
        self.message         = respones.message

        if not respones.slots:
            return 
        
        self.song_id   = respones.slots[0].song_id
        self.song_name = respones.slots[0].song_name
        self.artist    = respones.slots[0].artist
        self.image     = respones.slots[0].image
        self.lyric     = respones.slots[0].lyric 
        self.result    = respones.slots[0].song_url

        if len(respones.slots) > 1:
           self.play_list       = respones.slots


