import sqlite3
from tkinter import Y
import numpy as np
import keras
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import time

# Retrieve data from the data base
DATABASE_PATH = "prices.sqlite"

def db_connection(path: str):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except sqlite3.Error as e:
        print("Error:", e)
    return connection

connection = db_connection(DATABASE_PATH)
cur = connection.cursor()

x = []
y = []

for row in cur.execute("SELECT * FROM prices"):
    x.append(row[2])
    y.append(row[1])

connection.close()

x_np = np.array(x)
print("x_np", x_np)
y_np = np.array(y)

max_x = np.max(x_np)
min_x = np.min(x_np)
x_scaled = (x_np-min_x)/(max_x-min_x)
print("x_scaled", x_scaled)

max_y = np.max(y_np)
min_y = np.min(y_np)
y_scaled = (y_np-min_y)/(max_y-min_y)
print("y_scaled", y_scaled)

x_train, x_validate, x_test = np.array_split(x_scaled, 3)
y_train, y_validate, y_test = np.array_split(y_scaled, 3)

# model
model = keras.Sequential()
model.add(keras.layers.Dense(12, input_dim=1, activation='relu'))
model.add(keras.layers.Dense(20, activation='relu'))
model.add(keras.layers.Dense(20, activation='elu'))
model.add(keras.layers.Dense(1, activation='linear'))

# compile
model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy'])

# fit
fitted = model.fit(x_train, y_train, epochs=250, batch_size=10, validation_data=(x_validate, y_validate))
# print(fitted.history)

# evaluate
loss, accuracy = model.evaluate(x_test, y_test)
print('Loss:', loss)

# predict
prediction = model.predict(x_test)
ax1 = plt.subplot()
l1 = ax1.plot(prediction, color="blue", label="prediction")
ax2 = plt.twinx()
l2 = ax2.plot(y_test, color="green", label="actual")
plt.legend(loc="upper left")
plt.title("Test set")
plt.show()

prediction = model.predict(x_validate)
ax1 = plt.subplot()
l1 = ax1.plot(prediction, color="blue", label="prediction")
ax2 = plt.twinx()
l2 = ax2.plot(y_test, color="green", label="actual")
plt.legend(loc="upper left")
plt.title("Validation set")
plt.show()

prediction = model.predict(x_train)
ax1 = plt.subplot()
l1 = ax1.plot(prediction, color="blue", label="prediction")
ax2 = plt.twinx()
l2 = ax2.plot(y_test, color="green", label="actual")
plt.legend(loc="upper left")
plt.title("Training set")
plt.show()