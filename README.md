# Nelly - Frame Based Conversational Agent.

Nelly is a Frame Based Conversational Agent for Sandwiches Ordering. Nelly is the final project for the Natural Language Interaction course of the Master in Intelligent Interactive Systems at the Department of Information and Communication Technologies of the [Universitat Pompeu Fabra, Barcelona, Spain.](https://www.upf.edu/)


### Build your own sandwich

Categories:
* Bread type (Mandatory)
* Vegetables
* Protein
* Sauce
* Cheese
* Food Restrictions


## Prerequisites

In order to run Nelly you will need to install the below libraries:

* spaCy is compatible with 64-bit CPython 2.7 / 3.5+ and runs on Unix/Linux, macOS/OS X and Windows:
```
pip install -U spacy
python -m spacy download en_core_web_sm
```

* gTTS (Google Text-to-Speech), a Python library and CLI tool to interface with Google Translate's text-to-speech API:
```
pip install gTTS
```

* SpeechRecognition, Library for performing speech recognition, with support for several engines and APIs, online and offline:
```
pip install SpeechRecognition

pip install pipwin
pipwin install pyaudio
```


## Enable Nelly

```
python listen_and_talk.py
```

## Authors

* **Georgios Angelopoulos** - [LinkedIn](https://www.linkedin.com/in/george-angelopoulos/)
* **Daniel Levkovits** - [LinkedIn](https://www.linkedin.com/in/daniellevkovits/)
* **Jorge Pimienta** - [LinkedIn](https://www.linkedin.com/in/jorge-p-364544a9/)
* **Cristian Morales** - [LinkedIn](https://www.linkedin.com/in/cmoraleso/)

## Acknowledgments

We would like to thank the Professors Leo Wanner and Mireia Farrús, for the guidance and advice they have provided us throughout the creation of Nelly.

