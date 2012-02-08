#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
