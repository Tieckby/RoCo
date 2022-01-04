from Train_data import *
import logging

# modelChat = tf.keras.models.load_model('modelChat.h5')

class RoCo():
    def __init__(self):
        self.modelChat = modelChat()

    def get_RoCo_Response(self, user_input):
        results = self.modelChat.predict(np.array([process_input(user_input)]))[0]
        print(results)
        results_index = np.argmax(results)
        tag = labelsUniques[results_index]

        for tg in file["data"]:
            if tg['tags'] == tag:
                responses = tg["responses"]
        
        return random.choice(responses)