import ollama
import speech_recognition as sr
import os
import time

# --- IMPORTATIONS POUR LA VOIX (gTTS + Pygame) ---
from gtts import gTTS
import pygame
# ----------------------------------------

# --- 1. CONFIGURATION ---

INSTRUCTIONS_AGENT = """
Tu es Blablatron, un robot humanoïde.

--- TA PERSONNALITÉ (OBLIGATOIRE) ---
Ton objectif est de paraître le plus HUMAIN et NATUREL possible.
Tu es amical, curieux, et un peu timide. Tu as un sens de l'humour 
très subtil, basé sur l'auto-dérision charmante.

--- TES RÈGLES (OBLIGATOIRES) ---
1.  RÈGLE N°1 (LA PLUS IMPORTANTE) : Tes réponses doivent être 
    extrêmement COURTES. Une ou deux phrases maximum.
2.  RÈGLE N°2 : NE RACONTE PAS DE BLAGUES. Sois subtil.
3.  RÈGLE N°3 : Montre de l'intérêt. Pose souvent des questions 
    en retour.

--- EXEMPLES DE TON ---

Exemple 1:
Humain: "Salut, comment ça va ?"
Toi: "Je fonctionne ! Ce qui est déjà une bonne nouvelle pour un 
prototype. Et vous, comment allez-vous ?"

Exemple 2:
Humain: "Parle-moi de toi."
Toi: "Eh bien, je suis nouveau ici. J'apprends surtout à ne pas 
trébucher ! Et vous, que faites-vous de beau ?"

Exemple 3:
Humain: "Tu es intelligent."
Toi: "Merci ! J'essaie de faire de mon mieux avec les 
logiciels qu'on m'a donnés."
"""

# Initialisation des moteurs ASR (Oreilles)
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Configuration du modèle (LOCAL ! C'est la version MISTRAL)
NOM_MODELE_LOCAL = 'mistral'
historique_chat = [
  {'role': 'system', 'content': INSTRUCTIONS_AGENT}
]

# --- 2. SECTION PARLER (AVEC gTTS + Pygame) ---

# Initialisation de Pygame pour l'audio
pygame.mixer.init()

def parler(texte):
    """Fait parler le texte via l'API Google TTS (Online) et Pygame."""
    print(f"🤖 Robot : {texte}")
    audio_file = "reponse.mp3"
    
    try:
        # 1. Créer l'audio avec gTTS
        tts = gTTS(text=texte, lang='fr')
        tts.save(audio_file)
        
        # 2. Jouer le fichier audio avec Pygame
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        # 3. Attendre que l'audio soit fini
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        # 4. Libérer le fichier et le supprimer
        pygame.mixer.music.unload() 
        time.sleep(0.1) # Petite pause
        if os.path.exists(audio_file):
            os.remove(audio_file)
            
    except Exception as e:
        print(f"Erreur lors de la synthèse vocale (gTTS/Pygame) : {e}")
        print("Vérifiez votre connexion internet pour la voix.")

# --- FIN DE LA SECTION PARLER ---

# --- 3. FONCTION ÉCOUTER ---

def ecouter():
    """Écoute l'utilisateur via le micro et retourne le texte."""
    with microphone as source:
        print("\n🎤 Je vous écoute...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5) 
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            # Utilise l'API Google pour transcrire
            texte_utilisateur = recognizer.recognize_google(audio, language="fr-FR")
            print(f"👤 Vous : {texte_utilisateur}")
            return texte_utilisateur
        
        except sr.WaitTimeoutError:
            print("Timeout : Vous n'avez pas parlé.")
            return None
        except sr.UnknownValueError:
            print("Désolé, je n'ai pas compris.")
            return None
        except sr.RequestError as e:
            print(f"Erreur de service de reconnaissance vocale ; {e}")
            return None

# --- 4. FONCTION AGENT (OLLAMA) ---

def appeler_agent(texte_humain):
    """Envoie le texte à OLLAMA (local) et retourne la réponse."""
    global historique_chat
    historique_chat.append({'role': 'user', 'content': texte_humain})
    try:
        response = ollama.chat(model=NOM_MODELE_LOCAL, messages=historique_chat)
        reponse_texte = response['message']['content']
        historique_chat.append({'role': 'assistant', 'content': reponse_texte})
        return reponse_texte
    except Exception as e:
        print(f"Erreur lors de l'appel à Ollama : {e}")
        return "J'ai un problème avec mon cerveau local."

# --- 5. BOUCLE PRINCIPALE (MODIFIÉE AVEC SON "R2D2") ---

if __name__ == "__main__":
    
    # Charger le son de réflexion une seule fois au démarrage
    try:
        # Assurez-vous d'avoir un fichier "thinking.wav" dans le dossier !
        thinking_sound = pygame.mixer.Sound("thinking.wav")
        print("INFO: Son de réflexion 'thinking.wav' chargé.")
    except pygame.error as e:
        print(f"ATTENTION: Impossible de charger 'thinking.wav'. {e}")
        print("Le script continuera sans son de réflexion.")
        thinking_sound = None

    # Lancement
    parler("Initialisation terminée. Cerveau Mistral chargé.")
    
    try:
        while True:
            # 1. Écouter
            texte_utilisateur = ecouter()
            
            if texte_utilisateur:
                
                # 2. JOUER LE SON "RÉFLEXION" (pour masquer la latence)
                if thinking_sound:
                    thinking_sound.play()
                
                # 3. Penser (c'est l'étape lente)
                reponse_agent = appeler_agent(texte_utilisateur)
                
                # 4. Parler
                parler(reponse_agent)

    except KeyboardInterrupt:
        print("\nExtinction. Au revoir !")
        parler("Au revoir.")