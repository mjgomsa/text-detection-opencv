
import config
import openai
from cvHandler import captureImageAndExtractText

openai.api_key = config.api_key


def askGPT(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{prompt}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    toreturn = response.choices[0].message['content'].strip()
    # print(toreturn)
    return toreturn


def get_extracted_text():
    title = captureImageAndExtractText()
    return title
    # return input("What book are you reading? ")


def get_book_title(extracted_text):
    prompt = f"Using the following string '{extracted_text}' identify which book it might be.  Please omit all introductory text or subsequent text! Again, only output the title of the book, no explanation, introduction, conclusion  or 'the book is__'."
    title = askGPT(prompt)
    return title


def get_book_genre(book_title):
    prompt = f"Based on the book title '{book_title}', determine the genre that the book fits into. Please omit all introductory text and use the following format: <comma_separated_list_of_book_genres>."
    book_genre = askGPT(prompt)
    return book_genre


def map_to_music_genre(book_genre):
    prompt = f"Based on the each of the book's genres '{book_genre}', map to a music genre. Such that for the following, the relationship is <Fiction Genre> : <Music Genre>. For example: \n Absurdist : New Wave, Adventure: March/Military, Alternate History: Gregorian Chant, Americana: Ragtime, Chick Literature: Pop, Coming of Age: Folk, Crime: Rap/Hip Hop, Cyberpunk: Industrial, Dickensian: Standards, Epic Fantasy: Progressive Metal, Erotica: Latin/Tango, Fable: Rock, Gothic: Black Metal, Historical: Baroque, Humor: Polka, Inspirational: Spiritual/Religious, Mystery: Blues, Poetry: Jazz, Pulp: Lounge, War: Death Metal, Romance: Love pop, etc. Please omit all introductory text and omit the book's genre, only output music genres in the following format: <comma_separated_list_of_music_genres>"
    music_genre = askGPT(prompt)
    return music_genre


def generate_sonic_pi_code(music_genre):
    prompt = f"Based on the music genres '{music_genre}', create the code for a song within the intersection of these music genres in Sonic Pi. Please omit all introductory text or subsequent text! Again, only output the code to be played in Sonic Pi, no explanation, introduction or conclusion to the code."
    music_code = askGPT(prompt)
    return music_code


def main():
    # extracted_text = get_extracted_text()
    # book_title = get_book_title(extracted_text)
    book_title = "Harry Potter"
    book_genre = get_book_genre(book_title)
    music_genre = map_to_music_genre(book_genre)
    sonic_pi_code = generate_sonic_pi_code(music_genre)

    print(f"Book Title: {book_title}")
    # print(f"Book Genre: {book_genre}")
    # print(f"Book Genre: {music_genre}")
    print("=== SONIC PI CODE ===")
    print(sonic_pi_code)


main()
