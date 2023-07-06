import numpy as np
from pickle import load
from keras.applications.xception import Xception, preprocess_input
from keras.utils import load_img, img_to_array
from keras.utils.data_utils import pad_sequences
from keras.utils import load_img, img_to_array
from keras.applications.xception import Xception, preprocess_input
from model import get_model
import json 

model = get_model()
tokenizer = load(open("hashtagApp/models/tokenizer.p","rb"))
xception_model = Xception( weights='hashtagApp/models/tf_imagenet_notop.h5',include_top=False, pooling="avg")
obj_model = Xception(weights='hashtagApp/models/tf_imagenet.h5')

def extract_features(image, model):
        image = image.resize((299,299))
        image = np.array(image)
        # for images that has 4 channels, we convert them into 3 channels
        if image.shape[2] == 4: 
            image = image[..., :3]
        image = np.expand_dims(image, axis=0)
        image = image/127.5
        image = image - 1.0
        feature = model.predict(image)
        return feature

def word_for_id(integer, tokenizer):
  for word, index in tokenizer.word_index.items():
      if index == integer:
          return word
  return None


def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'start'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        pred = model.predict([photo,sequence], verbose=0)
        pred = np.argmax(pred)
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'end':
            break
    return in_text

def clean_description(text):
    return " ".join(text.split()[1:-1])

def get_text_info(image):
    photo = extract_features(image, xception_model)
    description = generate_desc(model, tokenizer, photo, max_length=32)
    description = clean_description(description)
    objects = get_objects(image, obj_model)
    return description + " \n " + " ".join(objects).replace("_"," ")

def decode_predictions(yhat, top=5):
    with open("hashtagApp/models/imagenet_class_index.json") as f:
        CLASS_INDEX = json.load(f)

    results = []
    for pred in yhat:
        top_indices = pred.argsort()[-top:][::-1]
        result = [tuple(CLASS_INDEX[str(i)]) + (pred[i],) for i in top_indices]
        result.sort(key=lambda x: x[2], reverse=True)
        results.append(result)

    return results

def get_objects(image, obj_model):
    image = image.resize((299, 299))
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the VGG model
    image = preprocess_input(image)
    # predict the probability across all output classes
    yhat = obj_model.predict(image)
    # convert the probabilities to class labels
    label = decode_predictions(yhat)
    # retrieve the most likely result, e.g. highest probability
    label = label[0][0:5]
    return [x[1] for x in label]

