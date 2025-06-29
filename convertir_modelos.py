import tensorflow as tf

# Cargar modelos .keras
modelo_temp = tf.keras.models.load_model("models/best_model.keras")
modelo_lluvia = tf.keras.models.load_model("models/best_model_lluvia.keras")

# Guardar como .h5
modelo_temp.save("models/best_model.h5")
modelo_lluvia.save("models/best_model_lluvia.h5")

print("Modelos convertidos a .h5")
