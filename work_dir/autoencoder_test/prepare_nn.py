
from keras.layers import Input, Dense, Flatten, Reshape
from keras.models import Model


def create_dense_autoencoder():
	
	encoding_dim = 49
	
	input_img = Input(shape = (28, 28, 1))
	flat_img = Flatten()(input_img)
	encoded = Dense(encoding_dim, activation = "relu")(flat_img)
	
	input_encoded = Input(shape = (encoding_dim,))
	flat_decoded = Dense(28 * 28, activation = "sigmoid")(input_encoded)
	
	decoded = Reshape((28, 28, 1))(flat_decoded)

	encoder = Model(input_img, encoded, name = "encoder")
	decoder = Model(input_encoded, decoded, name = "decoder")
	autoencoder = Model(input_img, decoder(encoder(input_img)), name = "autoencoder")
	
	return encoder, decoder, autoencoder

	
