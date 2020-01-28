

'''

Very simple neural network created by bsaund to practice coding in 
Tensorflow 2.0 (instead of 1.0)

'''

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
import data_tools
import IPython


class SimpleNetwork:
    def __init__(self):
        self.build_example_model()


    def simple_pass(self):
        W = tf.Variable(tf.ones(shape=(2,2)), name="W")
        b = tf.Variable(tf.zeros(shape=(2)), name="b")

        @tf.function
        def forward(x):
            return W * x + b

        out_a = forward([1,0])
        print(out_a)
    
    #     self.W = tf.Variable(tf.ones(shape=(2,2)), name="W")
    #     self.b = tf.Variable(tf.ones(shape=(2)), name="b")

    # @tf.function
    # def forward(self, x):
    #     return self.W * x + self.b
    

    def build_example_model(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, 3, activation='relu',
                                   kernel_regularizer=tf.keras.regularizers.l2(0.04),
                                   input_shape=(28, 28, 1)),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dropout(0.1),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(10, activation='softmax')
        ])

    def forward_model(self):
        train_data = tf.ones(shape=(1, 28, 28, 1))
        test_data = tf.ones(shape=(1, 28, 28, 1))
        
        train_out = self.model(train_data, training=True)
        print("Train out")
        print(train_out)


        test_out = self.model(test_data, training=False)
        print()
        print("Test out")
        print(test_out)


class AutoEncoder:
    def __init__(self):
        self.side_length = 64
        self.num_voxels = self.side_length ** 3

        self.checkpoint_path = "training_checkpoints/cp.ckpt"
        self.model = None
        
        self.build_autoencoder_network()

    def restore(self):
        # self.model = tf.keras.models.load_model(self.checkpoint_path)
        self.model.load_weights(self.checkpoint_path)


    def build_autoencoder_network(self):
        ip = (self.side_length, self.side_length, self.side_length, 1)
        self.model = tf.keras.Sequential([
            # tf.keras.layers.Flatten(),
            # tf.keras.layers.Dense(self.num_voxels, activation='softmax')
            tf.keras.layers.Conv3D(64, (2,2,2), input_shape=ip, padding="same"),
            tf.keras.layers.Activation(tf.nn.relu),
            tf.keras.layers.MaxPool3D((2,2,2)),

            tf.keras.layers.Conv3D(128, (2,2,2), input_shape=ip, padding="same"),
            tf.keras.layers.Activation(tf.nn.relu),
            tf.keras.layers.MaxPool3D((2,2,2)),

            tf.keras.layers.Conv3D(256, (2,2,2), input_shape=ip, padding="same"),
            tf.keras.layers.Activation(tf.nn.relu),
            tf.keras.layers.MaxPool3D((2,2,2)),

            tf.keras.layers.Conv3D(512, (2,2,2), input_shape=ip, padding="same"),
            tf.keras.layers.Activation(tf.nn.relu),
            tf.keras.layers.MaxPool3D((2,2,2)),

            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(2000, activation='relu'),
            
            tf.keras.layers.Dense(32768, activation='relu'),
            tf.keras.layers.Reshape((4,4,4,512)),
            

            tf.keras.layers.Conv3DTranspose(256, (2,2,2,), strides=2),
            tf.keras.layers.Activation(tf.nn.relu),
            tf.keras.layers.Conv3DTranspose(128, (2,2,2,), strides=2),
            tf.keras.layers.Activation(tf.nn.relu),
            tf.keras.layers.Conv3DTranspose(64, (2,2,2,), strides=2),
            tf.keras.layers.Activation(tf.nn.relu),
            tf.keras.layers.Conv3DTranspose(1, (2,2,2,), strides=2),

        ])

        self.model.compile(optimizer='adam',
                           # loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                           loss=tf.keras.losses.MSE, 
                           metrics=[tf.keras.metrics.MeanAbsoluteError()])

    def count_params(self):
        # tots = len(tf.training_variables())
        # print("There are " + str(tots) + " training variables")
        self.model.summary()
        
    def train(self, dataset):
        self.count_params()

        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=self.checkpoint_path,
                                                         save_weights_only=False,
                                                         verbose=1)
        
        self.model.fit(dataset.repeat(10), epochs=10,
                       callbacks=[cp_callback])

    def train_and_test(self, dataset):
        dataset.shuffle(10000)

        train_ds = dataset.skip(100)
        test_ds = dataset.take(100)
        # IPython.embed()
        self.train(train_ds.batch(16))

    def evaluate(self, dataset):
        self.model.evaluate(dataset.batch(16))
        



if __name__ == "__main__":
    print("hi")
    sn = SimpleNetwork()
    # sn.simple_pass()
    sn.forward_model()
