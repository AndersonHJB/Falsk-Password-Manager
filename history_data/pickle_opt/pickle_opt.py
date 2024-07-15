import pickle

with open('data/admins.pickle', 'rb') as file:
    loaded_admins = pickle.load(file)

print(loaded_admins)
for item in loaded_admins:
    print(item)