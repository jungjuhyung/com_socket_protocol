from scipy import interpolate
import numpy as np

class DataLogger:
    def __init__(self):
        self.source_Data_Set = []
        self.assesment_Data_Set = []

    def source_Data_Update(self, f_que, s_que, c_que):
        f_data = f_que.get()
        s_data = s_que.get()
        c_data = c_que.get()

        x_train_front_8 = f_data.IR_ARR_8
        x_train_front_64 = f_data.IR_ARR_64
        x_train_side_8 = s_data.IR_ARR_8
        x_train_side_64 = s_data.IR_ARR_64
        x_train_ceil_8 = c_data.IR_ARR_8
        x_train_ceil_64 = c_data.IR_ARR_64

        x_train_front_8 = self.Preprocess_MM_IMG(x_train_front_8)  ## 전처리 수정코드
        x_train_front_8 = self.Preprocess_SIG_IMG(x_train_front_8)  ## 전처리 수정코드
        x_train_front_8 = x_train_front_8.reshape(8, 8, 1).astype("float32")
        f_data.IR_ARR_8 = x_train_front_8

        x_train_side_8 = self.Preprocess_MM_IMG(x_train_side_8)  ## 전처리 수정코드
        x_train_side_8 = self.Preprocess_SIG_IMG(x_train_side_8)  ## 전처리 수정코드
        x_train_side_8 = x_train_side_8.reshape(8, 8, 1).astype("float32")
        s_data.IR_ARR_8 = x_train_side_8

        x_train_ceil_8 = self.Preprocess_MM_IMG(x_train_ceil_8)  ## 전처리 수정코드
        x_train_ceil_8 = self.Preprocess_SIG_IMG(x_train_ceil_8)  ## 전처리 수정코드
        x_train_ceil_8 = x_train_ceil_8.reshape(8, 8, 1).astype("float32")
        c_data.IR_ARR_8 = x_train_ceil_8

        x_train_front_64 = self.Preprocess_MM_IMG(x_train_front_64)  ## 전처리 수정코드
        x_train_front_64 = self.Preprocess_SIG_IMG(x_train_front_64)  ## 전처리 수정코드
        x_train_front_64 = x_train_front_64.reshape(64,64,1).astype("float32")
        f_data.IR_ARR_64 = x_train_front_64

        x_train_side_64 = self.Preprocess_MM_IMG(x_train_side_64)  ## 전처리 수정코드
        x_train_side_64 = self.Preprocess_SIG_IMG(x_train_side_64)  ## 전처리 수정코드
        x_train_side_64 = x_train_side_64.reshape(64,64,1).astype("float32")
        s_data.IR_ARR_64 = x_train_side_64

        x_train_ceil_64 = self.Preprocess_MM_IMG(x_train_ceil_64)  ## 전처리 수정코드
        x_train_ceil_64 = self.Preprocess_SIG_IMG(x_train_ceil_64)  ## 전처리 수정코드
        x_train_ceil_64 = x_train_ceil_64.reshape(64,64,1).astype("float32")
        c_data.IR_ARR_64 = x_train_ceil_64

        dict_data = {
            "res_idx":f_data.res_idx,
             "f_Source_DAta":f_data,
             "s_Source_DAta":s_data,
             "c_Source_DAta":c_data
        }
        self.source_Data_Set.append(dict_data)

    def assessment_Data_Update(self, assessment_Data):
        self.assesment_Data_Set.append(assessment_Data)


    def Preprocess_MM_IMG(self, IR_img):
        min_nor_dist_val = -5
        max_nor_dist_val = 5

        min_val = np.min(IR_img)
        max_val = np.max(IR_img)

        Pre_mm_IR_img_ = ((IR_img - min_val) / (max_val - min_val)) * (
                    max_nor_dist_val - min_nor_dist_val) + min_nor_dist_val

        return Pre_mm_IR_img_


    def sigmoid(self,x):
        return 1 / (1 + np.exp(-x))

    def Preprocess_SIG_IMG(self, Pre_mm_IR_img_):
        # print("Preprocess SIGn Func Call")
        Pre_sig_IR_img_ = self.sigmoid(Pre_mm_IR_img_)

        return Pre_sig_IR_img_


