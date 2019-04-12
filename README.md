# Speeks – Improves public speaking

### It is an application which revolve around solving the public speaking problems and act as personal public speaking analyser which detect your flaws and help you improving your public speaking/speaking skills.

The analysis of the content would be done in following **parameters** :
* Grammar check
* Speech emotion recognition 
* Confidence level
* Expression detection

**Grammar** would be analysed under these broad categories:
* Grammartical errors
    * Superlative/comparitive
    * Adverb placement
    * Sentence fragment
    * Duplicate words
    * Missing prepositions

* Verb
    * Missing verb
    * Gerund with subortinating conjuction

* Determiner
    * Definite/Indefinite articles
    * A/An placements
    * Quantifier misuse

* Pronouns 
    * Subject and Object
    * Missing reflexive
    * Who/Whom context



![image](https://user-images.githubusercontent.com/24489162/55281759-5257e000-535f-11e9-9a65-418642ff7551.png)


**Speech emotion recognition** would detect the sentiments of the audio file and will provide with the probability that the content have anger, calm, happy, sad and fearfull.

We divide our audio file in chunks of 2.5 seconds then the result of these chunks are analyzed using graphical representation of each 25 second chunks


![image](https://user-images.githubusercontent.com/26388073/55283405-0f5a3480-5380-11e9-97df-08f38c0d232e.png)

**Confidence level detection**
We would be using VGGish model time distributed LSTM for confidence level detection.This would provide us with per second confidence level of the speaker which can be further analysed to detect which part of the speech was most confident and which was the least confident and how the confidnce level fluctuates during whole speech

![image](https://user-images.githubusercontent.com/26388073/55283451-382ef980-5381-11e9-8579-f340e0282328.png)

**Expression detection** would be done with VGGFace model.This would give us the facial expression per frame of the speaker.
These expressions include angry, disgust, fear, happy, sad, surprise, neutral.

![image](https://user-images.githubusercontent.com/26388073/55283525-e8513200-5382-11e9-96d7-2048763b9428.png)

Using all these parameters we would analyse the speech of the speaker.

According to the MIT research paper on language acoustic 2009 these were among the parameters which define the quality of speech 

## Architecture and Workflow
![image](https://user-images.githubusercontent.com/26388073/55283457-6dd3e280-5381-11e9-9bb7-db0434457673.png)

> [Product Hunt](https://www.producthunt.com/posts/speeks)
