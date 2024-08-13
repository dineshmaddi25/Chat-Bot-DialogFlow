import speech_recognition as sr
import difflib

# Initialize the recognizer
recognizer = sr.Recognizer()
def get_audio(timeout=10):
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            print('Listening...')
            audio = recognizer.listen(source, timeout=timeout)  # Set a timeout for listening
            command = recognizer.recognize_google(audio)
            command = command.lower()
            print(f"Recognized text: {command}")
            return command
    except sr.WaitTimeoutError:
        print('Timeout exceeded. No speech detected.')
    except sr.UnknownValueError:
        print('Speech recognition could not understand audio.')
    except sr.RequestError as e:
        print(f'Speech recognition request failed: {e}')
    return ""  # Return an empty string if no speech is detected or an error occurs


def preprocess_text(text):
    words = text.split()
    new_words = []
    for i in range(len(words)):
        if i == 0 or words[i] != words[i - 1]:
            new_words.append(words[i])
    preprocessed_text = ' '.join(new_words)
    return preprocessed_text

def compare_texts(input_text, recognized_text):
    # Preprocess recognized text to remove repetitions
    recognized_text = preprocess_text(recognized_text)
    sequence_matcher = difflib.SequenceMatcher(None, input_text, recognized_text)
    similarity_ratio = sequence_matcher.ratio()
    match_percentage = similarity_ratio * 100
    return match_percentage


# Main loop
while True:
    try:
        input_text = input("Enter the text string you want to speak: ")

        if not input_text:
            print("No input text provided. Please try again.")
            continue

        recognized_text = get_audio()
        if recognized_text:
            match_percentage = compare_texts(input_text, recognized_text)
            print(f"Match Percentage: {match_percentage:.2f}%")
        else:
            print("No speech detected. Match Percentage: 0.00%")

    except KeyboardInterrupt:
        print("Program terminated by user.")
        break
