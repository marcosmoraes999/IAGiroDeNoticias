# coding: utf-8
import os
import shutil
from os import listdir
from os.path import isfile, join
import gpt_2_simple as gpt2
import subprocess
import sys
import logging
import stringUtils as s
import re

#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
folder = "C:\\Users\\Pichau\\github\\transformers\\examples\\"
run_generation = "run_generation.py"
def generateTextWithGPT2(prefix, length, numSamples, prob):
    prefix = s.cleanSentence(prefix)
    logging.debug("Texto recebido pela GPT2: " + prefix)

    import random
    if os.path.isfile("INTERRUPT_GPT2_SENTENCES"):
        os.remove("INTERRUPT_GPT2_SENTENCES")
        subprocess.run(args=['python', folder + run_generation, '--model_type=gpt2', '--model_name_or_path=gpt2-xl', '--prompt=' + prefix + '', '--length='+str(length), '--seed='+str(random.randint(0, 999999999)), '--num_samples='+str(numSamples), '--temperature=1.0','--prob=' + str(prob), '--stop_token=.'], shell = True)
        return True
    else:
        subprocess.run(args=['python', folder + run_generation, '--model_type=gpt2', '--model_name_or_path=gpt2-xl', '--prompt=' + prefix + '', '--length='+str(length), '--seed='+str(random.randint(0, 999999999)), '--num_samples='+str(numSamples), '--prob=' + str(prob), '--temperature=1.0'], shell = True)
        return False

def downloadGPT2Model(modelSize = "simple"):
    if(modelSize.lower() == "simple"):
        model_name = "124M"
    elif(modelSize.lower() == "medium"):
        model_name = "355M"
    elif(modelSize.lower() == "large"):
        model_name = "774M"
    else:
        model_name = "1558M"

    if not os.path.isdir(os.path.join("models", model_name)):
        print(f"Downloading {model_name} model...")
        gpt2.download_gpt2(model_name=model_name)

def trainModel(dictionary, model_size = "124M"):
    text = ""
    for eachItem in dictionary.items():
        for eachItemArticle in eachItem:
            if(type(eachItemArticle) == int):
                continue
            else:
                text += eachItemArticle["texto"] + " "
    f = open("data.txt", "w+")
    f.write(text)
    f.close()
    gpt2.encode_dataset("data.txt")

def finetuneModel(model_size = "124M"):
    sess = gpt2.start_tf_sess()
                #gpt2.load_gpt2(sess)
                #gpt2.generate(sess, prefix="My name is ")
    gpt2.finetune(sess, dataset = "text_encoded.npz", model_name = model_size, overwrite = True, steps = 10)
                #return

def textGeneration(model_size = "124M"):
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name='run1')
    gpt2.generate(sess, model_name = model_size, nsamples = 4)
    #print(text)
    #model.generate_batch_from_prompts("teste")

def generateText(initialText):
    prob = 0.0
    text = ""
    if os.path.exists("generated.txt"):
        os.remove("generated.txt")
    while(True):
        logging.debug("Texto recebido pelo GPT-2: " + text)
        endProcedure = generateTextWithGPT2(s.cleanSentence(initialText) + s.cleanSentence(text), 10, 20, prob)

        f = open("generated.txt", "r")
        for x in f:
            text += x
        text = s.cleanSentence(text)
        f.close()

        logging.debug("Texto lido no arquivo: " + text)
        if(endProcedure):
            f = open("generated.txt", "w")
            f.write(text)
            f.close()
            return text
        prob += 0.15
