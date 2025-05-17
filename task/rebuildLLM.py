from app.core.core import RetraineLR, RetraineSGD
from app.core.keras import KerasLLM, KerasMultiFeatureLLM
import os

kerasllm = KerasLLM()
kerasMF = KerasMultiFeatureLLM()

class TaskLLm:
    def __init__(self):
        
        super().__init__()
        return
    def delModels(self):
        os.remove('./LLMmodels/keras_llm.keras.keras')
        os.remove('./LLMmodels/keras_multi_llm.keras')
        os.remove('./LLMmodels/LineareRegretion.pkl')
        os.remove('./LLMmodels/sgdRegretion.pkl')
        return
    def lineareregretionTaine(self,):
        RetraineLR()
        self.delModels()
        return
    def sgdregretionTaine(self,):
        RetraineSGD()
        return
    def retraineKeras(self):
        kerasllm.train_model()
        kerasMF.train_model()
        return