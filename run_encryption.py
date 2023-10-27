from main import run_encryption


secret_message = '''You discover that home is not a person or a place
But a feeling you can't get back'''

original_imagePATH = 'image.jpg'

encrypted_imagePATH = 'encoded_image.png'

initial_colorCode = (0, 0)

step_size = 1


run_encryption(secret_message, original_imagePATH, encrypted_imagePATH, initial_colorCode, step_size)
