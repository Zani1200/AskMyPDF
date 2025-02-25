class Handler:

    def __init__(self):
        pass

    def limpiarPrompt(self, prompt):
        prompt_limpio = prompt.strip()
        prompt_lowerCase = prompt_limpio.lower()
        return prompt_lowerCase

    def comprobarClave(self, response):
        if response == "videojuegos" or "Videojuegos":
            return True
        else:
            return False

