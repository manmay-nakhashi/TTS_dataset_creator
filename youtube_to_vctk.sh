# yt-dlp --no-playlist -a $1
yt-dlp -a $1
find . -name "* *" -type f | rename 's/ /_/g'
for i in *.webm; do ffmpeg -i $i ${i::-5}.wav; done
mkdir audio_files
mv *.wav audio_files
mkdir video_files
mv *.webm video_files

mkdir split_audio
for i in audio_files/*; do ffmpeg -i $i -f segment -segment_time 500 -c copy split_audio/${i:12:-5}_%03d.wav; done

mkdir cleaned_audio
for i in split_audio/*; do spleeter separate -p spleeter:2stems -o cleaned_audio/ $i -d 500; done   
for i in cleaned_audio/*/; do ffmpeg -y -i $i/vocals.wav -af arnndn=m=rnnoise-models/beguiling-drafter-2018-08-30/bd.rnnn $i/vocals_ns.wav; done
for i in cleaned_audio/*/; do ffmpeg -y -i $i/vocals_ns.wav -af "volume=1" $i/vocals.wav; done

mkdir $2
mv split_audio cleaned_audio video_files audio_files $2

for i in $2/cleaned_audio/*/vocals.wav; do whisperx $i --language en --hf_token <hftoken> --diarize --min_speakers 1 --max_speakers 2 --output_dir ${i::-10}; done
python3 cut_and_export.py $2/cleaned_audio/