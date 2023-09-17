import random
import string

def generate_secret_key(length=32):
  """Generates a random secret key of the specified length.

  Args:
    length: The length of the secret key to generate.

  Returns:
    A random secret key of the specified length.
  """
  characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
  key = ''.join(random.choice(characters) for _ in range(length))
  return key

if __name__ == '__main__':
  print(generate_secret_key())