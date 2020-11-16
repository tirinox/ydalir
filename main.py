from bit import Key, PrivateKey, PrivateKeyTestnet

key = PrivateKey()

print('Я родился!')
print(key.address)
print(key.get_balance())
