import base64

import aiofiles


async def decode_music_file(music_file):
    """Декодирвоание mp3 файла"""
    async with aiofiles.open(music_file, mode="rb") as file_like:
        data = file_like.read()
        decoded_data = base64.b64decode(data)
        yield decoded_data
