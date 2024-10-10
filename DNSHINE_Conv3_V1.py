import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, utils
import matplotlib.pyplot as plt

train_size_8 = 30000
test_size_8 = 10000
train_size_64 = 30000  # 필요한 경우 조정
test_size_64 = 10000  # 필요한 경우 조정
input_shape_8 = (8, 8, 1)
input_shape_64 = (64, 64, 1)
num_classes = 8  # 클래스 수

def loading_slicing_Train(file):
    raw_set = np.loadtxt(file, delimiter=',', dtype=np.float32)
    x_data = raw_set[:, 0:-1]
    y_data = raw_set[:, [-1]]
    return x_data, y_data

def loading_slicing_Test(file):
    raw_set = np.loadtxt(file, delimiter=',', dtype=np.float32)
    x_data = raw_set[:, 0:-1]
    y_data = raw_set[:, [-1]]
    return x_data, y_data

def Preprocess_MM_IMG(IR_img):
    min_nor_dist_val = -5
    max_nor_dist_val = 5
    max_array_ = []
    min_array_ = []
    Pre_mm_IR_img_ =[]
    
    for i in range(len(IR_img)):
        min_val = np.min(IR_img[i])
        max_val = np.max(IR_img[i])
        max_array_.append(max_val)
        min_array_.append(min_val)
        
    for i in range(len(IR_img)):
        Pre_mm_IR_img_temp = ((IR_img[i] - min_array_[i])/(max_array_[i]-min_array_[i])) * (max_nor_dist_val - min_nor_dist_val) + min_nor_dist_val
        Pre_mm_IR_img_.append(Pre_mm_IR_img_temp)

    Pre_mm_IR_img_ = np.array(Pre_mm_IR_img_)
    return Pre_mm_IR_img_

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def Preprocess_SIG_IMG(Pre_mm_IR_img_temp):
    #print("Preprocess SIGn Func Call")
    Pre_sig_IR_img_ = []
    Pre_mm_IR_img_temp = np.array(Pre_mm_IR_img_temp)  # 리스트를 NumPy 배열로 변환
    for i in range(len(Pre_mm_IR_img_temp)):
        Pre_sig_IR_img_temp = sigmoid(Pre_mm_IR_img_temp[i])
        Pre_sig_IR_img_.append(Pre_sig_IR_img_temp)
        
    Pre_sig_IR_img_ = np.array(Pre_sig_IR_img_)    
    return Pre_sig_IR_img_

# 8x8 입력 데이터에 대한 로드 및 전처리
x_train_front_8, y_train_front_8 = loading_slicing_Train('../Dataset/train_front.csv')
x_train_front_8 = Preprocess_MM_IMG(x_train_front_8)   ## 전처리 수정코드
x_train_front_8 = Preprocess_SIG_IMG(x_train_front_8)   ## 전처리 수정코드
x_train_front_8 = x_train_front_8.reshape(train_size_8, 8, 8, 1).astype("float32")
y_train_front_8 = utils.to_categorical(y_train_front_8.astype("uint32"), num_classes)

x_test_front_8, y_test_front_8 = loading_slicing_Test('../Dataset/test_front.csv')
x_test_front_8 = Preprocess_MM_IMG(x_test_front_8)   ## 전처리 수정코드
x_test_front_8 = Preprocess_SIG_IMG(x_test_front_8)   ## 전처리 수정코드
x_test_front_8 = x_test_front_8.reshape(test_size_8, 8, 8, 1).astype("float32")
y_test_front_8 = utils.to_categorical(y_test_front_8.astype("uint32"), num_classes)
##############################################################3
x_train_side_8, y_train_side_8 = loading_slicing_Train('../Dataset/train_side.csv')
x_train_side_8 = Preprocess_MM_IMG(x_train_side_8)   ## 전처리 수정코드
x_train_side_8 = Preprocess_SIG_IMG(x_train_side_8)   ## 전처리 수정코드
x_train_side_8 = x_train_side_8.reshape(train_size_8, 8, 8, 1).astype("float32")
y_train_side_8 = utils.to_categorical(y_train_side_8.astype("uint32"), num_classes)

x_test_side_8, y_test_side_8 = loading_slicing_Test('../Dataset/test_side.csv')
x_test_side_8 = Preprocess_MM_IMG(x_test_side_8)   ## 전처리 수정코드
x_test_side_8 = Preprocess_SIG_IMG(x_test_side_8)   ## 전처리 수정코드
x_test_side_8 = x_test_side_8.reshape(test_size_8, 8, 8, 1).astype("float32")
y_test_side_8 = utils.to_categorical(y_test_side_8.astype("uint32"), num_classes)
##############################################################3
x_train_ceiling_8, y_train_ceiling_8 = loading_slicing_Train('../Dataset/train_ceiling.csv')
x_train_ceiling_8 = Preprocess_MM_IMG(x_train_ceiling_8)   ## 전처리 수정코드
x_train_ceiling_8 = Preprocess_SIG_IMG(x_train_ceiling_8)   ## 전처리 수정코드
x_train_ceiling_8 = x_train_ceiling_8.reshape(train_size_8, 8, 8, 1).astype("float32")
y_train_ceiling_8 = utils.to_categorical(y_train_ceiling_8.astype("uint32"), num_classes)

x_test_ceiling_8, y_test_ceiling_8 = loading_slicing_Test('../Dataset/test_ceiling.csv')
x_test_ceiling_8 = Preprocess_MM_IMG(x_test_ceiling_8)   ## 전처리 수정코드
x_test_ceiling_8 = Preprocess_SIG_IMG(x_test_ceiling_8)   ## 전처리 수정코드
x_test_ceiling_8 = x_test_ceiling_8.reshape(test_size_8, 8, 8, 1).astype("float32")
y_test_ceiling_8 = utils.to_categorical(y_test_ceiling_8.astype("uint32"), num_classes)
##############################################################3


# 64x64 입력 데이터에 대한 로드 및 전처리
x_train_front_64, y_train_front_64 = loading_slicing_Train('../Dataset/train_front_64.csv')
x_train_front_64 = Preprocess_MM_IMG(x_train_front_64)   ## 전처리 수정코드
x_train_front_64 = Preprocess_SIG_IMG(x_train_front_64)   ## 전처리 수정코드
x_train_front_64 = x_train_front_64.reshape(train_size_64, 64, 64, 1).astype("float32")
y_train_front_64 = utils.to_categorical(y_train_front_64.astype("uint32"), num_classes)

x_test_front_64, y_test_front_64 = loading_slicing_Test('../Dataset/test_front_64.csv')
x_test_front_64 = Preprocess_MM_IMG(x_test_front_64)   ## 전처리 수정코드
x_test_front_64 = Preprocess_SIG_IMG(x_test_front_64)   ## 전처리 수정코드
x_test_front_64 = x_test_front_64.reshape(test_size_64, 64, 64, 1).astype("float32")
y_test_front_64 = utils.to_categorical(y_test_front_64.astype("uint32"), num_classes)
##############################################################3
x_train_side_64, y_train_side_64 = loading_slicing_Train('../Dataset/train_side_64.csv')
x_train_side_64 = Preprocess_MM_IMG(x_train_side_64)   ## 전처리 수정코드
x_train_side_64 = Preprocess_SIG_IMG(x_train_side_64)   ## 전처리 수정코드
x_train_side_64 = x_train_side_64.reshape(train_size_64, 64, 64, 1).astype("float32")
y_train_side_64 = utils.to_categorical(y_train_side_64.astype("uint32"), num_classes)

x_test_side_64, y_test_side_64 = loading_slicing_Test('../Dataset/test_side_64.csv')
x_test_side_64 = Preprocess_MM_IMG(x_test_side_64)   ## 전처리 수정코드
x_test_side_64 = Preprocess_SIG_IMG(x_test_side_64)   ## 전처리 수정코드
x_test_side_64 = x_test_side_64.reshape(test_size_64, 64, 64, 1).astype("float32")
y_test_side_64 = utils.to_categorical(y_test_side_64.astype("uint32"), num_classes)
##############################################################3
x_train_ceiling_64, y_train_ceiling_64 = loading_slicing_Train('../Dataset/train_ceiling_64.csv')
x_train_ceiling_64 = Preprocess_MM_IMG(x_train_ceiling_64)   ## 전처리 수정코드
x_train_ceiling_64 = Preprocess_SIG_IMG(x_train_ceiling_64)   ## 전처리 수정코드
x_train_ceiling_64 = x_train_ceiling_64.reshape(train_size_64, 64, 64, 1).astype("float32")
y_train_ceiling_64 = utils.to_categorical(y_train_ceiling_64.astype("uint32"), num_classes)

x_test_ceiling_64, y_test_ceiling_64 = loading_slicing_Test('../Dataset/test_ceiling_64.csv')
x_test_ceiling_64 = Preprocess_MM_IMG(x_test_ceiling_64)   ## 전처리 수정코드
x_test_ceiling_64 = Preprocess_SIG_IMG(x_test_ceiling_64)   ## 전처리 수정코드
x_test_ceiling_64 = x_test_ceiling_64.reshape(test_size_64, 64, 64, 1).astype("float32")
y_test_ceiling_64 = utils.to_categorical(y_test_ceiling_64.astype("uint32"), num_classes)
##############################################################3
batch_size = 16 #64
epochs = 50 # 150

# Define the model using the Functional API

# Function to create a branch for 8x8 input
def create_branch_8(input_shape):
    input = layers.Input(shape=input_shape)
    x = layers.Conv2D(64, (3, 3), padding="same", activation="relu")(input)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
    x = layers.Conv2D(128, (3, 3), padding="same", activation="relu")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
#    x = layers.Conv2D(256, (3, 3), padding="same", activation="relu")(x) # ADD LAYER
#    x = layers.MaxPooling2D(pool_size=(2, 2))(x) # ADD LAYER
    output = layers.Flatten()(x)
    return models.Model(inputs=input, outputs=output)

# Function to create a branch for 64x64 input
def create_branch_64(input_shape):
    input = layers.Input(shape=input_shape)
    x = layers.Conv2D(32, (3, 3), padding="same", activation="relu")(input)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
    x = layers.Conv2D(64, (3, 3), padding="same", activation="relu")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
    x = layers.Conv2D(128, (3, 3), padding="same", activation="relu")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
    x = layers.Conv2D(256, (3, 3), padding="same", activation="relu")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
    x = layers.Conv2D(512, (3, 3), padding="same", activation="relu")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
    #x = layers.Conv2D(1024, (3, 3), padding="same", activation="relu")(x) # ADD LAYER
    #x = layers.MaxPooling2D(pool_size=(2, 2))(x) # ADD LAYER
    output = layers.Flatten()(x)
    return models.Model(inputs=input, outputs=output)

# Create 3 branches for 8x8 input
branch_8_1 = create_branch_8(input_shape_8)
branch_8_2 = create_branch_8(input_shape_8)
branch_8_3 = create_branch_8(input_shape_8)

# Create 3 branches for 64x64 input
branch_64_1 = create_branch_64(input_shape_64)
branch_64_2 = create_branch_64(input_shape_64)
branch_64_3 = create_branch_64(input_shape_64)

# Combine the outputs of all branches
combined = layers.concatenate([
    branch_8_1.output,
    branch_8_2.output,
    branch_8_3.output,
    branch_64_1.output,
    branch_64_2.output,
    branch_64_3.output
])

# Fully connected layers and final softmax output
z = layers.Dense(4096, activation="relu")(combined)
z = layers.Dense(1024, activation="relu")(z)
z = layers.Dense(256, activation="relu")(z)
z = layers.Dense(64, activation="relu")(z)
z = layers.Dense(32, activation="relu")(z)
final_output = layers.Dense(num_classes, activation="softmax")(z)

# Create the model
model = models.Model(inputs=[
    branch_8_1.input,
    branch_8_2.input,
    branch_8_3.input,
    branch_64_1.input,
    branch_64_2.input,
    branch_64_3.input
], outputs=final_output)

model.summary()

# Compile the model
model.compile(
    loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
)

# Train the model
hist = model.fit(
    [
	x_train_front_8, x_train_side_8, x_train_ceiling_8,
	x_train_front_64, x_train_side_64, x_train_ceiling_64
    ], y_train_front_8,  # Assuming y_train_8 == y_train_64
    batch_size=batch_size, epochs=epochs, validation_split=0.3
)

# Plot training results
fig, loss_ax = plt.subplots()
acc_ax = loss_ax.twinx()

loss_ax.plot(hist.history['loss'], 'y', label='train loss')
loss_ax.plot(hist.history['val_loss'], 'r', label='val loss')
loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
loss_ax.legend(loc='upper left')

acc_ax.plot(hist.history['accuracy'], 'b', label='train acc')
acc_ax.plot(hist.history['val_accuracy'], 'g', label='val acc')
acc_ax.set_ylabel('accuracy')
acc_ax.legend(loc='upper right')

plt.show()

# Evaluate the model
score = model.evaluate([
	x_test_front_8, x_test_side_8, x_test_ceiling_8,
	x_test_front_64, x_test_side_64, x_test_ceiling_64
], y_test_front_8, verbose=0)  # Assuming y_test_8 == y_test_64
print("Test loss:", score[0])
print("Test accuracy:", score[1])

# Save the model
model.save('DNSHINE_Model3_Conv3.h5')
