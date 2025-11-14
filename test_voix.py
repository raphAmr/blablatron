import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')

print("--- Test audio des voix disponibles ---")
print("Écoutez attentivement...")

for i, voice in enumerate(voices):
    print(f"\nTest VOIX {i} : {voice.name}")
    try:
        engine.setProperty('voice', voice.id)
        
        # Test en français pour Hortense
        if 'fr-FR' in voice.languages:
            engine.say(f"Ceci est un test de la voix française, {voice.name}.")
        # Test en anglais pour les autres
        else:
            engine.say(f"This is a test of the voice {voice.name}.")
            
        engine.runAndWait()
    except Exception as e:
        print(f"  Erreur avec cette voix: {e}")

print("\n-------------------------------------")
print("Test terminé.")