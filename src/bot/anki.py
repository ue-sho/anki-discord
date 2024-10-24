from bot.anki_connect import invoke
from bot.anki_gpt import generate_note
from bot.settings import settings
from bot.english import add_audio_to_text, fetch_image_url


def get_all_decks() -> dict:
    response = invoke(action="deckNames")
    data = response["result"]
    return data


def get_deck_stats(deckName: str) -> dict:
    params = {"decks": [deckName]}
    response = invoke(action="getDeckStats", **params)
    first_key = next(iter(response["result"]))
    data = response["result"][first_key]
    return data


def create_deck(deckName: str) -> None:
    params = {"deck": deckName}
    response = invoke(action="createDeck", **params)
    data = response["result"]
    return data


def delete_deck(deckName: str, cardsToo: bool = True) -> dict:
    params = {"decks": [deckName], "cardsToo": cardsToo}
    response = invoke(action="deleteDecks", **params)
    data = response["result"]
    return data


def delete_decks(decks: list[str], cardsToo: bool = True) -> dict:
    params = {"decks": decks, "cardsToo": cardsToo}
    response = invoke(action="deleteDecks", **params)
    data = response["result"]
    return data


def add_note(json: dict) -> dict:
    params = {"note": json}
    response = invoke(action="addNote", **params)
    data = response["result"]
    return data


def sync_decks() -> dict:
    response = invoke(action="sync")
    data = response["result"]
    return data


def add_to_anki(text: str) -> dict:
    english_word = generate_note(text)
    text_with_audio = add_audio_to_text(text)
    image = fetch_image_url(text)

    note_json = {
        "deckName": settings.deck_name,
        "modelName": "Basic",
        "fields": {
            "front": text_with_audio,
            "example": english_word.example.replace("\n", "<br>").replace(
                text, f'<span style="color:red;">{text}</span>'
            ),
            "meaning": english_word.meaning,
            "etymology": english_word.etymology,
            "situation": english_word.situation,
        },
        "options": {"allowDuplicate": False},
        "tags": [],
        "audio": [
            {
                "url": "https://cdn.videvo.net/videvo_files/video/free/2015-06/small_watermarked/Contador_Glam_preview.mp4",
                "filename": "countdown.mp4",
                "fields": ["front"],
            }
        ],
        "picture": [{"url": image, "filename": "black_cat.jpg", "fields": ["image"]}],
    }
    res = add_note(note_json)

    return res