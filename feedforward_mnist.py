
from tensorflow import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import Dropout
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
import numpy as np

#Data loading and modification

#load in famous mnist dataset (number classification with 28x28 images)
(x_train, y_train), (x_test, y_test) = mnist.load_data()
#normalizing images (pixel values) such that the entire training and test set have a mean of 0 and standard deviatinon of 1 (optimal learning, see my post about activation functions)
x_train= (x_train - np.mean(x_train))/np.std(x_train)
x_test= (x_test - np.mean(x_test))/np.std(x_test)
#do the train test split such that it is a 80-10-10 split
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.1)

#creating the model
model = Sequential([
    #the input is 2d, this is not possible with a feedforward neural network
    #so we flatten the input to a 1d row of inputs
    Flatten(input_shape=(28, 28)),
    Dense(256, activation="relu"),
    #add some dropout to prevent overftitting
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),
    #add some dropout to prevent overftitting
    Dropout(0.3),
    Dense(32, activation='relu'),
    #mnist has 10 digits, so 10 sepeprate output nodes using the softmax activation function
    Dense(10, activation='softmax')
])
#setting the learning optimizer (adam is standard), a specific loss function for categorical problems and we care about accuracy, so use this as metric
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

#save the best model
checkpoint = ModelCheckpoint('best_model.keras', save_best_only=True, monitor='val_accuracy', mode='max')

#train the model
model.fit(x_train, y_train, epochs=20, validation_data=(x_val, y_val), callbacks=[checkpoint], verbose=2, batch_size=64)

#load the best model and evaluate performance on test set
keras.models.load_model("best_model.keras")
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
