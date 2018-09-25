from os import listdir,getcwd
from os.path import isfile, join
import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

from keras import backend as K
K.set_image_dim_ordering('tf')

from keras.utils import np_utils
from keras.models import Sequential
from keras.optimizers import SGD,RMSprop,adam
from keras.models import Model, load_model
from keras.layers import Input, Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense

img_rows = 128
img_col = 128
num_channel = 1


label = []
img_list_data =[]

path = getcwd()+'\\22_dataset'


files_name =[f for f in listdir(path) if isfile(join(path, f))
            and f != '.DS_Store']
print('\nTotal Number of images in Dataset {}'.format(len(files_name)))


# 1. Pre-Processing
for name in files_name:
    input_image = cv2.imread(join(path,name))
    input_image = cv2.cvtColor(input_image,cv2.COLOR_BGR2GRAY)
    input_image_resize = cv2.resize(input_image,(img_rows,img_col))
    img_list_data.append(input_image_resize)
    label.append(int(name.split('_')[1].split('.')[0]))

img_data = np.array(img_list_data)
img_data = img_data.astype('float32')
img_data /= 255
print(img_data.shape)
if num_channel ==1:
    img_data = np.expand_dims(img_data, axis=4)
    print("image shape",img_data[0].shape)


# defining classes
num_classes = 3
names =['left', 'forward', 'right']


Y = np_utils.to_categorical(y=label, num_classes=num_classes)

#shuffle the dataset
x,y = shuffle(img_data,Y,random_state=2)
# split
X_train, X_test, y_train , y_test = train_test_split(x,y, test_size=0.2, random_state=2)

input_shape = img_data[0].shape
print(input_shape)

#defining model
model = Sequential()
model.add(Conv2D(32,(3,3),input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(32,(3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dense(34))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))
model.compile(optimizer='adam',loss='mean_squared_error',metrics=["accuracy"])
model.summary()
#score = model.evaluate(X_test, y_test, show_accuracy=True, verbose=0)
#print('Test Loss:', score[0])
#
# print('Test accuracy:', score[1])

from keras import callbacks
model_path = getcwd()+'\\best_autopilot(with_Car_test).hdf5'

#Save the model after each epoch if the validation loss improved.
save_best = callbacks.ModelCheckpoint(model_path, monitor='val_loss', verbose=1,
                                     save_best_only=True, mode=
                                      'min')

#stop training if the validation loss doesn't improve for 5 consecutive epochs.
early_stop = callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=5,
                                     verbose=0, mode='auto')

callbacks_list = [save_best, early_stop]
#only  uncomment if gona continue traning
#model = load_model(model_path)

history =model.fit(X_train, y_train, batch_size=64, epochs=50, validation_data=(X_test, y_test), callbacks=callbacks_list)

model = load_model(model_path)
P = model.predict(img_data[:700:10])
print(model.predict_classes(img_data[:700:10]))


from sklearn.metrics import classification_report,confusion_matrix
import itertools

Y_pred = model.predict(X_test)
print(Y_pred)
y_pred = np.argmax(Y_pred,axis=1)
print(y_pred)

traget_names = ['class0(forward)','class1(right)', 'class2(left)']
print(classification_report(np.argmax(y_test,axis=1),y_pred,target_names=traget_names))
print(confusion_matrix(np.argmax(y_test,axis=1),y_pred))
cnf_matrix = (confusion_matrix(np.argmax(y_test,axis=1), y_pred))

np.set_printoptions(precision=2)

plt.figure()
from plot_conf import  plot_confusion_matrix



plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
plot_confusion_matrix(cnf_matrix,classes=traget_names,title='Confusion matrix')

plt.show()