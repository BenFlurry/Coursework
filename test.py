import hashlib
string = 'hello world'
encoded = string.encode()
print(encoded)
result = hashlib.sha256(encoded)
print(result)
hex = result.hexdigest()
print(hex)

self.password = hashlib.sha256(self.password1.encode()).hexdigest()

