import glob
import pandas as pd
from pydub import AudioSegment
from pathlib import Path
import sys
def get_speaker_times(filename):
    speaker_times = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        start_time = None
        end_time = None
        speaker = None
        prev_speaker = None
        for line in lines:
            line = line.strip()
            if '-->' in line:
                start_time, end_time = line.split('-->')
                start_time = start_time.strip()
                end_time = end_time.strip()
                prev_speaker = speaker
            elif line.isdigit():
                if speaker is not None and prev_speaker != speaker and speaker != "UNKNOWN":
                    speaker_times.append([speaker, int(start_time.replace(':', '').replace(',',''))])
            elif line.startswith('['):
                speaker = line.split(']')[0][1:]
    return speaker_times

wav_folders = glob.glob(sys.argv[1]+"/*")
print(wav_folders)
output_folder = "output/wavs/"
txt_folder = "output/txt"
Path(output_folder).mkdir(parents=True, exist_ok=True)
Path(txt_folder).mkdir(parents=True, exist_ok=True)
counter = 0
for folder in wav_folders:
    print(folder)
    time_stamps = pd.read_csv(folder+"/vocals.tsv", sep="\t")
    speaker_times = get_speaker_times(folder+"/vocals.word.srt")
    for ts in range(len(speaker_times) - 1):
        time_stamps_frame = time_stamps[(time_stamps["end"] <= speaker_times[ts+1][1]) & (time_stamps["start"] >= speaker_times[ts][1])]
        print(speaker_times[ts][0], speaker_times[ts][1])
        for index, row in time_stamps_frame.iterrows():
            start_time = row["start"]
            end_time = row["end"]
            wav = AudioSegment.from_wav(folder+"/vocals.wav")
            chunk=wav[start_time:end_time]
            Speaker_folder = speaker_times[ts][0]
            Path(output_folder+"/"+folder+"/"+Speaker_folder).mkdir(parents=True, exist_ok=True)
            Path(txt_folder+"/"+folder+"/"+Speaker_folder).mkdir(parents=True, exist_ok=True)
            chunk.export(output_folder+"/"+folder+"/"+Speaker_folder+"/"+str(counter)+'.wav', format="wav")
            with open(txt_folder+"/"+folder+"/"+Speaker_folder+"/"+str(counter)+'.txt', "w+") as f:
                f.write(row["text"])
            counter+=1
    time_stamps_frame = time_stamps[time_stamps["start"] >= speaker_times[-1][1]]
    print(speaker_times[-1][0], speaker_times[-1][1])
    for index, row in time_stamps_frame.iterrows():
        start_time = row["start"]
        end_time = row["end"]
        wav = AudioSegment.from_wav(folder+"/vocals.wav")
        chunk=wav[start_time:end_time]
        Speaker_folder = speaker_times[-1][0]
        Path(output_folder+"/"+folder+"/"+Speaker_folder).mkdir(parents=True, exist_ok=True)
        Path(txt_folder+"/"+folder+"/"+Speaker_folder).mkdir(parents=True, exist_ok=True)
        chunk.export(output_folder+"/"+folder+"/"+Speaker_folder+"/"+str(counter)+'.wav', format="wav")
        with open(txt_folder+"/"+folder+"/"+Speaker_folder+"/"+str(counter)+'.txt', "w+") as f:
                f.write(row["text"])
        counter+=1