#!/usr/bin/env python
#-*- coding: utf-8 -*-

from video2rockbox.config import *
from os import popen, system

def get_model_info(model):
  for manufacturer in models:
    if models[manufacturer].get(model):
      return models[manufacturer][model]
      break

def video_resolution(input_file):
  com = 'ffmpeg -i "%s" 2>&1 | grep "Video:" | grep -Eo "[0-9]{2,4}x[0-9]{2,4}"' % input_file
  raw = popen(com).read()
  out = raw.split('\n')[0].split('x')
  return (int(out[0]), int(out[1]))



class Video:
  def __init__(self, model, input_file,
                output_file=False, video_rate=False, audio_rate=False):

    self.model = model
    self.input_file = input_file
    self.model_info = self.get_full_info()
    self.input_resolution = self.get_video_resolution()
    self.output_resolution = self.out_resolution()
    self.video_rate = 400
    self.audio_rate = 128

    if output_file:
      self.output_file = output_file
    else:
      self.out_file_name()


  def get_full_info(self):
    return get_model_info(self.model)
  def get_video_resolution(self):
    return video_resolution(self.input_file)

  def out_file_name(self):
    infile_list = self.input_file.split('.')
    infile_list[-1] = 'mpeg'
    self.output_file = '.'.join(infile_list)

  def out_resolution(self):
    video_ar = float(self.input_resolution[0]) / float(self.input_resolution[1])
    player_ar = float(resolutions[self.model_info[0]][0]) / float(resolutions[self.model_info[0]][1])

    if video_ar == player_ar:
      return resolutions[self.model_info[0]]
    elif video_ar > player_ar:
      return (resolutions[self.model_info[0]][0], int(resolutions[self.model_info[0]][0] / video_ar))
    else:
      return (int(resolutions[self.model_info[0]][1] * video_ar), resolutions[self.model_info[0]][1])

  def convert(self, two_pass=True):
    pass2 = ''
    if two_pass:
      pass2 = '-pass 2'
      values_pass1 = (
        self.input_file,
        self.output_resolution[0],
        self.output_resolution[1],
        self.output_file,
      )
      
      command_pass1 = 'ffmpeg -i "%s" -vcodec mpeg2video\
      -b 100k -an -s %ix%i -r 23 -mbd rd -trellis 2\
      -cmp 2 -subcmp 2 -g 100 -pass 1 "%s"' % values_pass1
      system(command_pass1)
    
    values_pass2 = (
      self.input_file,
      self.video_rate,
      self.audio_rate,
      self.output_resolution[0],
      self.output_resolution[1],
      pass2,
      self.output_file,
    )
    
    command_pass2 = 'ffmpeg -i "%s" -vcodec mpeg2video\
    -b %ik -ac 2 -ab %ik -acodec libmp3lame -s %ix%i\
    -r 23 -mbd rd -trellis 2 -cmp 2 -subcmp 2 -g 100\
    %s -y "%s"' % values_pass2
    system(command_pass2)

