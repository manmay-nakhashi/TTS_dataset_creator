# TTS_dataset_creator
create dataset from list of youtube links easily
# setup repo
```
git clone https://github.com/m-bain/whisperX
git clone https://github.com/GregorR/rnnoise-models.git
```
install ffmpeg > 5.0 for rnnnoise support
for using different rnnnoise model
you can change rnnnoise path in th bash script.

```
conda install -c conda-forge ffmpeg==5.1.0
```

setup whisperx

```
$ git clone https://github.com/m-bain/whisperX.git
$ cd whisperX
$ pip install -e .
```
Speaker Diarization
To enable Speaker. Diarization, include your Hugging Face access token that you can generate from Here after the --hf_token argument and accept the user agreement for the following models: Segmentation , Voice Activity Detection (VAD) , and Speaker Diarization

update this hf_token in youtube_to_vctk.sh script

add all the links in one txt file
and then run
youtube_to_vctk.sh links.txt out_folder_name

vctk dataset will be in output folder.
