#!/usr/bin/env python
#-*- coding: utf-8 -*-

from config import *
from optparse import OptionParser
from os import system
from subprocess import Popen, PIPE

full_model_info = ()
video_res = ()

def GetResolution(infile):
  com = 'ffmpeg -i "%s" 2>&1 | grep "Video:" | grep -Eo "[0-9]{2,4}x[0-9]{2,4}"' % infile
  raw = Popen(com, shell=True, stdin=PIPE, stdout=PIPE).stdout.read()
  out = str(raw).replace('\\n\'', '').replace('b\'', '').split('x')
  return (int(out[0]), int(out[1]))

def ShowModels():
  stdout = ''
  for manufacturer in models:
    if models[manufacturer]:
      stdout += '%s:\n' % manufacturer
      for model in models[manufacturer]:
        stdout += '\t%i: %s\n' % (model, models[manufacturer][model][1])
      stdout += '\n'
  return stdout

parser = OptionParser()
parser.add_option('-m', '--model', dest='model', help='Player model number. For list all suported models: --models-list or -l.', metavar='<int>')
parser.add_option('-i', '--input-file', dest='input_file', help='Path to input file.', metavar='<str>')
parser.add_option('-o', '--output-file', dest='output_file', help='Path to output file.', metavar='<str>')
parser.add_option('-v', '--video-rate', dest='v_rate', help='Video bitrate.', metavar='<int>')
parser.add_option('-a', '--audio-rate', dest='a_rate', help='Audio bitrate.', metavar='<int>')
parser.add_option('-l', '--models-list', dest='models_list', action='store_true', help='Show all models.', default=False)

options, args = parser.parse_args()

try:
  model = int(options.model)
except:
  model = 0
try:
  input_file = options.input_file
except:
  input_file = False
try:
  output_file = str(options.output_file)
except:
  output_file = '%s.mpeg' % input_file
try:
  video_rate = int(options.v_rate)
except:
  video_rate = 400
try:
  audio_rate = int(options.a_rate)
except:
  audio_rate = 128

if options.models_list:
  print(ShowModels())

if not input_file or input_file == None:
  exit()

for manufacturer in models:
  if models[manufacturer].get(model):
    full_model_info = models[manufacturer][model]
    break

#Get video resolution and calculate resolution of out file
video_res = GetResolution(input_file)

if video_res:
  video_ar = video_res[0] / video_res[1]
  player_ar = resolutions[full_model_info[0]][0] / resolutions[full_model_info[0]][1]

if video_ar == player_ar:
  resolution = '%ix%i' % resolutions[full_model_info[0]]
elif video_ar > player_ar:
  resolution = '%ix%i' % (resolutions[full_model_info[0]][0], int(resolutions[full_model_info[0]][0] / video_ar))
else:
  resolution = '%ix%i' % (int(resolutions[full_model_info[0]][1] * video_ar), resolutions[full_model_info[0]][1])


#Convert video
system('ffmpeg -i "%s" -vcodec mpeg2video -b 100k -an -s %s -r 23 -mbd rd -trellis 2 -cmp 2 -subcmp 2 -g 100 -pass 1 "%s"' % (input_file, resolution, output_file))

system('ffmpeg -i "%s" -vcodec mpeg2video -b %ik -ac 2 -ab %ik -acodec libmp3lame -s %s -r 23 -mbd rd -trellis 2 -cmp 2 -subcmp 2 -g 100 -pass 2 -y "%s"' % (input_file, video_rate, audio_rate, resolution, output_file))
