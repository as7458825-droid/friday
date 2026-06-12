from audioread import available_backends

print("Available backends:", [b.__name__ for b in available_backends()])
