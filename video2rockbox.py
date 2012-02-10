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
  out = str(raw)[2:-3].split('x')
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

def OutFileName(infile):
  infile_list = infile.split('.')
  infile_list[-1] = 'mpeg'
  outfile = '.'.join(infile_list)
  return outfile

def SetResolution(res, fmi):
  if res:
    ar = res[0] / res[1]
    player_ar = resolutions[fmi[0]][0] / resolutions[fmi[0]][1]

  if ar == player_ar:
    resolution = '%ix%i' % resolutions[fmi[0]]
  elif ar > player_ar:
    resolution = '%ix%i' % (resolutions[fmi[0]][0], int(resolutions[fmi[0]][0] / ar))
  else:
    resolution = '%ix%i' % (int(resolutions[fmi[0]][1] * ar), resolutions[fmi[0]][1])
  return resolution

parser = OptionParser()
parser.add_option('-m', '--model', dest='model', help='Player model number. For list all suported models: --models-list or -l.', metavar='<int>')
parser.add_option('-i', '--input-file', dest='input_file', help='Path to input file.', metavar='<str>')
parser.add_option('-o', '--output-file', dest='output_file', help='Path to output file.', metavar='<str>')
parser.add_option('-v', '--video-rate', dest='v_rate', help='Video bitrate.', metavar='<int>')
parser.add_option('-a', '--audio-rate', dest='a_rate', help='Audio bitrate.', metavar='<int>')
parser.add_option('-l', '--models-list', dest='models_list', action='store_true', help='Show all models.', default=False)

options, args = parser.parse_args()

if options.models_list:
  print(ShowModels())

if options.input_file == None or options.model == None:
  exit()

model = int(options.model)
input_file = str(options.input_file)

if options.output_file == None:
  output_file = OutFileName(input_file)
else:
  output_file = str(options.output_file)

try:
  video_rate = int(options.v_rate)
except:
  video_rate = 400

try:
  audio_rate = int(options.a_rate)
except:
  audio_rate = 128

for manufacturer in models:
  if models[manufacturer].get(model):
    full_model_info = models[manufacturer][model]
    break

#Get video resolution and calculate resolution of out file
video_res = GetResolution(input_file)
resolution = SetResolution(video_res, full_model_info)

#Convert video
system('ffmpeg -i "%s" -vcodec mpeg2video -b 100k -an -s %s -r 23 -mbd rd -trellis 2 -cmp 2 -subcmp 2 -g 100 -pass 1 "%s"' % (input_file, resolution, output_file))

system('ffmpeg -i "%s" -vcodec mpeg2video -b %ik -ac 2 -ab %ik -acodec libmp3lame -s %s -r 23 -mbd rd -trellis 2 -cmp 2 -subcmp 2 -g 100 -pass 2 -y "%s"' % (input_file, video_rate, audio_rate, resolution, output_file))
