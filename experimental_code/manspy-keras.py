import numpy
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input, Dropout


dataset = [
    {'word': 'montras', 'pos': 'verb'},
    {'word': 'vidas', 'pos': 'verb'},
    {'word': 'diras', 'pos': 'verb'},
    {'word': 'iras', 'pos': 'verb'},
    {'word': 'liras', 'pos': 'verb'},
    {'word': 'domo', 'pos': 'noun'},
    {'word': 'monero', 'pos': 'noun'},
    {'word': 'banko', 'pos': 'noun'},
    {'word': 'kurso', 'pos': 'noun'},
    {'word': 'dolaro', 'pos': 'noun'},
    {'word': 'fenestro', 'pos': 'noun'},
    {'word': 'patro', 'pos': 'noun'},
    {'word': 'patrino', 'pos': 'noun'},
    {'word': 'fato', 'pos': 'noun'},
]

classes = ['verb', 'noun']
count_inputs = 10
count_outputs = len(classes)

model = Sequential([
    Input(shape=(count_inputs,)),
    Dense(20, activation='relu'),
    Dropout(0.5),
    Dense(count_outputs, activation='softmax'),
])

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy'],
)


def prepare_word(word):
    x = word.rjust(count_inputs, '\x00').encode()
    return [i/255 for i in list(x)]


x_train = []
y_train = []
for data in dataset:
    # x = data['word'].rjust(count_inputs, '\x00').encode()
    # x = [i/255 for i in list(x)]
    x = prepare_word(data['word'])
    x_train.append(x)

    y = [0] * count_outputs
    y[classes.index(data['pos'])] = 1
    y_train.append(y)

x_train = numpy.array(x_train)
y_train = numpy.array(y_train)

# print(x_train.shape)
# print(y_train.shape)
# print(x_train)
# print(y_train)

history = model.fit(
    x_train,
    y_train,
    batch_size=1,
    epochs=5,
    verbose=1,
    validation_split=0.1,
)

print()
print('stop')
print()

x_test = x_train
y_test = y_train
score = model.evaluate(x_test, y_test, batch_size=2)
# print('score:', score)

words = [
    'nano',
    'vegas',
    'iras',
]
x = [prepare_word(word) for word in words]
y = model(numpy.array(x))
for y_index, y_one in enumerate(y):
    print()
    print(words[y_index])
    for name, value in zip(classes, y_one):
        print(name, '=', float(value))

# print(dir(model))
# print(model.weights)
