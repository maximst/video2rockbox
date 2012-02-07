#!/usr/bin/python3
#-*- coding: utf-8 -*-

from optparse import OptionParser
from os import system

full_model_info = ()
Q = 0.0
AR = 0
resolutions = (
  ('320x240', '320x200', '320x180'),
  ('220x166', '220x138', '220x124'),
  ('176x128', '176x110', '176x100'),
  ('160x120', '160x100', '160x90'),
  ('138x104', '138x86', '138x78'),
  ('128x96', '128x80', '128x72'),
  ('106x80', '128x80', '132x74'),
)
models = {
  'Archos':{
    
  },
  'iRiver':{
    10:(3, 'H120/H140'),
    11:(1, 'H320/H340'),
    14:(3, 'H10 20Gb'),
    15:(5, 'H10 5/6Gb'),
  }
  'Apple iPod':{
    20:(1, 'Color/Photo'),
    21:(2, 'Nano 1G'),
    22:(0, 'Video'),
    24:(0, '4G Grayscale'), #?
    25:(4, 'Mini 1G'),
    26:(4, 'Mini 2G'),
    27:(0, '1G, 2G'), #?
    28:(2, 'Nano 2G'),
  }
  'Cowon/iAudio':{
    30:(3, 'X5/X5V/X5L'),
    31:(3, 'M5/M5L'),
  }
  'Toshiba':{
    40:(0, 'Gigabeat F/X'),
    41:(0, 'Gigabeat S'),
  }
  'SanDisk':{
    50:(1, 'Sansa e200'),
    52:(6, 'Sansa c200'),
    56:(1, 'Sansa e200v2'),
    58:(1, 'Sansa Fuze'),
    63:(1, 'Sansa Fuze v2'),
    64:(0, 'Sansa Fuze+'),
  },
  'Olympus':{
    70:(0, 'M:Robe 100'), #?
  },
  'Logik':{
    
  },
  'Creative':{
    
  },
  'Philips':{
    
  },
  'Meizu':{
    
  },
  'Onda':{
    
  },
  'Lyre project':{
    
  },
  'Samsung':{
    
  },
  'Tatung':{
    
  },
  'Packard Bell':{
    
  },
  'MPIO':{
    
  },
  'HiFiMAN':{
    
  },
}

parser = OptionParser()
parser.add_option('-m', '--model', dest='model', help='Player model. For list all suported models: --models-list or -l.', metavar='<int>')
parser.add_option('-i', '--input-file', dest='input_file', help='Path to input file.', metavar='<str>')
parser.add_option('-o', '--output-file', dest='output_file', help='Path to output file.', metavar='<str>')
parser.add_option('-v', '--video-rate', dest='v_rate', help='Video bitrate.', metavar='<int>')
parser.add_option('-a', '--audio-rate', dest='a_rate', help='Audio bitrate.', metavar='<int>')
parser.add_option('-l', '--models-list', help='Audio bitrate.')

options, args = parser.parse_args()

try:
  model = int(options.model)
except:
  model = 0
try:
  input_file = str(options.input_file)
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


for manufacturer in models:
  if models[manufacturer].get(model):
    full_model_info = models[manufacturer][model]
    break

Q = 4/3
AR = 0

system('ffmpeg -i "%s" -vcodec mpeg2video -b 100k -an -s %s -r 23 -mbd rd -trellis 2 -cmp 2 -subcmp 2 -g 100 -pass 1 "%s"' % (input_file, resolutions[full_model_info[0]][AR], output_file))

system('ffmpeg -i "%s" -vcodec mpeg2video -b %ik -ac 2 -ab %ik -acodec libmp3lame -s %s -r 23 -mbd rd -trellis 2 -cmp 2 -subcmp 2 -g 100 -pass 2 -y "%s"' % (input_file, video_rate, audio_rate, resolutions[full_model_info[0]][AR], output_file))
