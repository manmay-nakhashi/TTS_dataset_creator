# yt-dlp --no-playlist -a $1
yt-dlp -a $1
find . -name "* *" -type f | rename 's/ /_/g'
for i in *.webm; do ffmpeg -i $i ${i::-5}.wav; done
#for i in *.mp4; do ffmpeg -i $i ${i::-4}.wav; done
mkdir audio_files
mv *.wav audio_files
mkdir video_files
mv *.webm video_files
#mv *.mp4 video_files
