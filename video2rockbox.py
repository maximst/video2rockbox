#!/usr/bin/env python
#-*- coding: utf-8 -*-

from video2rockbox.config import *
from optparse import OptionParser
from video2rockbox.converter import Video


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

if options.models_list:
  print(ShowModels())

if options.input_file == None or options.model == None:
  exit()

model = int(options.model)
input_file = options.input_file
output_file = options.output_file

try:
  video_rate = int(options.v_rate)
except:
  video_rate = 400

try:
  audio_rate = int(options.a_rate)
except:
  audio_rate = 128

converter = Video(model, input_file, output_file=output_file, video_rate=video_rate, audio_rate=audio_rate)

converter.Convert()
