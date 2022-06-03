from flask import Flask, request, jsonify, render_template
from keras.models import load_model
from keras.preprocessing import image
import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub


app = Flask(__name__, template_folder="client")
model = tf.keras.models.load_model(('MODEL/model_identification_plants.h5'), custom_objects={'KerasLayer': hub.KerasLayer})
df_info = pd.read_csv("info_tanaman.csv")
unique_label = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
IMAGE_SIZE = 224
df_barang = pd.read_csv('info_barang.csv')



def preprocess_image(image_path, labels=None):
    # read image
    image_data = tf.io.read_file(image_path)
    # turn jpeg into numbers
    image_data = tf.image.decode_jpeg(image_data, channels=3)
    # scaling / normalize (0,255) menjadi (0,1)
    image_data = tf.image.convert_image_dtype(image_data, dtype=tf.float32)
    # resize to (224,224)
    image_data = tf.image.resize(image_data, size=[IMAGE_SIZE, IMAGE_SIZE])
    return image_data, labels


def predict_label(img_path):
    test_images = [img_path]
    test_set = tf.data.Dataset.from_tensor_slices((tf.constant(test_images)))
    test_set = test_set.map(preprocess_image)
    test_set = test_set.batch(batch_size=32)
    test_predictions = model.predict(test_set)
    return unique_label[np.argmax(test_predictions)]


def get_herbal_info(herbal_id):
    data_info = df_info[df_info.id == herbal_id]
    herbal = data_info.tanaman.values[0]
    herbal_info = data_info.informasi.values[0]
    herbal_manfaat = data_info.manfaat.values[0]
    herbal_pengolahan = data_info.pengolahan.values[0]
    return herbal, herbal_info, herbal_manfaat, herbal_pengolahan

def get_barang_info(herbal_id, minPrice, maxPrice):
    message = "Tanaman yang berhasil ditemukan"
    result = df_barang.copy()
    result.butuh = result.butuh
    result.harga = result.harga
    result = result[(result.id_tanaman == herbal_id) & ((result.harga >= minPrice) & (result.harga <= maxPrice))]
    if result.shape[0] == 0:
        result = df_barang.copy()
        result.butuh = result.butuh
        result.harga = result.harga
        result = result[(result.id_tanaman == herbal_id)]
        message = "Tanaman dengan harga Rp "+str(minPrice)+"-"+str(maxPrice)+". Berikut list tanaman yang tersedia."
    result = result.sort_values(by=['nama_daun', 'harga'])
    return result.to_dict(orient='records'), message


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/app", methods=['GET'])
def main():
    return render_template("app.html")


@app.route("/list_data", methods=['POST'])
def get_list():
    return {'name': 'kiara'}


@app.route("/plants_analysis", methods=['POST'])
def plants_analysis():
    minPrice = int(request.form['minimumPrice'])
    maxPrice = int(request.form['maximumPrice'])

    leafImg = request.files['leafImage']
    img_path = "static/" + leafImg.filename
    leafImg.save(img_path)
    herbal_id = predict_label(img_path)

    herbal, herbal_info, herbal_manfaat, herbal_pengolahan = get_herbal_info(herbal_id)
    list_barang, message = get_barang_info(herbal_id, minPrice, maxPrice)

    response = jsonify({
        'herbal_result': herbal,
        'herbal_info': herbal_info,
        'manfaat_info': herbal_manfaat,
        'pengolahan_info': herbal_pengolahan,
        'recommendation': list_barang,
        'message': message
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    print(response)
    return response



if __name__ == '__main__':
    app.run(debug=True)
