from pytube import YouTube,Search
from moviepy.editor import *
from pytube import Playlist
import os
import time

'''
s = Search('Ethereal 15 sec, Steve Oxen Royalty free music, no copyright')

yt = s.results[0]
stream = yt.streams.filter(only_audio=True).first()
stream.download('Users/Swansy')
print(stream.title)


video = VideoFileClip(f'10 second chill music #7 | best to relax to!.mp4')
print(video.duration)
video.audio.write_audiofile(f'10 second chill music #7 | best to relax to!.mp3')

directories=[]
for d in os.listdir('Users'):
    directories.append(f'Users\\{d}')
for d in directories:
    print(d[6:])
    for song in os.listdir(d):
        print(song)

print('Podaj wage')
waga = input()

for i in range(len(waga)):
    print(i)
'''
p = Playlist('https://www.youtube.com/playlist?list=PLgzbsEOTETT0yxA0woGhzGqy4mnKOtCGW')
print(f'Downloading: {p.title}')
for video in p.videos:
    print(video.title)
    video.streams.filter(only_audio=True).first().download('Users/Wiktoria')
