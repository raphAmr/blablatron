import edge_tts
import pygame
import asyncio
import os

# --- Voix à tester ---
VOIX_HENRI = "fr-FR-HenriNeural"
VOIX_HORTENSE = "fr-FR-HortenseNeural"

TEXTE_TEST = "Bonjour, ceci est un test de ma voix. J'espère qu'elle vous plaît."

# --- Fonctions de test ---

# Initialisation de Pygame pour l'audio
pygame.mixer.init()

async def generer_et_jouer(texte, voix, nom_fichier):
    """Génère un fichier audio et le joue."""

    print(f"\n🎧 Test de la voix : {voix}")

    # Générer l'audio
    communicate = edge_tts.Communicate(texte, voix)
    await communicate.save(nom_fichier)

    # Jouer l'audio
    pygame.mixer.music.load(nom_fichier)
    pygame.mixer.music.play()

    # Attendre que l'audio soit fini
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload() 
    os.remove(nom_fichier)

async def main():
    print("Lancement du test des voix Edge TTS...")

    # Test 1: Hortense (Féminine)
    await generer_et_jouer(TEXTE_TEST, VOIX_HORTENSE, "hortense_test.mp3")

    # Test 2: Henri (Masculine)
    await generer_et_jouer(TEXTE_TEST, VOIX_HENRI, "henri_test.mp3")

    print("\nTest terminé.")

if __name__ == "__main__":
    asyncio.run(main())