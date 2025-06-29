from sklearn.preprocessing import MinMaxScaler
import numpy as np

def escalar_y_secuenciar(df, features, label, sequence_length):
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(df[features])
    sequences, labels = [], []
    for i in range(len(data_scaled) - sequence_length):
        sequences.append(data_scaled[i:i + sequence_length])
        labels.append(df[label].iloc[i + sequence_length])
    return np.array(sequences), np.array(labels), scaler
