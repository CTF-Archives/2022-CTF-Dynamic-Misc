# Author: Po7mn1
# Date: 2022/10/21
import wave
import numpy as np
import os
import random
from scipy.io.wavfile import write
import binascii
from flask import Flask, send_from_directory
from scipy.io import wavfile
duration = 60                 # 秒数
sampling_freq = 48000         # 频率
tone_freq = 2000
sampling_freq, audio = wavfile.read("c34257e2256d0daa568559b7ee7c1609.wav")
flag = ""
flag_scaled = ""
audio_sca = ""
hiddenFake = ""
hiddenFlag = ""
junk = ""
fake = ""
os.system("zip -P 'i1@mn!s*(e' /ajsiodjasodjasoijdasojsoidjsaoidj10293819023.zip /flag")  # zip -P 'i1@mn!s*(e' flag_zip.zip /flag
with open('/ajsiodjasodjasoijdasojsoidjsaoidj10293819023.zip', 'rb') as f:
     data = f.readlines()
     for i in data:
          hex_str = binascii.b2a_hex(i).decode('unicode_escape')
          flag += (str(hex_str))
junk = random.randint(50,100)
fake = '504B03040A000000000034BC55555252AB05550000005500000008000000666C61672E747874E4BDA0E698AFE68782E58E8BE7BCA9E58C85E79A84EFBC8CE4BD86E5BE88E98197E686BEEFBC8C666C6167E4B88DE59CA8E58E8BE7BCA9E58C85E9878CEFBC8CE5868DE689BEE689BEE380822D725975316E736572504B01023F000A000000000034BC55555252AB055500000055000000080024000000000000002000000000000000666C61672E7478740A00200000000000010018002176DD7D62E5D8012176DD7D62E5D8019046BC5462E5D801504B050600000000010001005A0000007B0000000E00666C6167D4DAC6E4CBFBB5D8B7BD' + 'A' * junk
fakeMake = []
for i in range(len(fake)):
     fakeMake.append(ord(fake[i]))
hiddenFake = np.array(fakeMake)
fake_scaled = np.int16(hiddenFake * 10)
cheat = random.randint(160000, 170000)
audio_sca = np.insert(audio, cheat, fake_scaled)
write('/asdiosajdiajoidjiaosdja.wav', sampling_freq, audio_sca)
sampling_freq, audio = wavfile.read("/asdiosajdiajoidjiaosdja.wav")
flagMake = []
cheat1 = random.randint(1805000, 1900000)
flag = str(flag) + 'A' * random.randint(10,40) 
for i in range(len(flag)):
     flagMake.append(ord(flag[i]))
hiddenFlag = np.array(flagMake)
flag_scaled_value = np.int16(hiddenFlag * 10)
flag_scaled = np.insert(audio, cheat1, flag_scaled_value)
write('/flag.wav', sampling_freq, flag_scaled)
app = Flask(__name__)
@app.route('/', methods=['GET'])
def displayFlag():
     return send_from_directory('/','flag.wav')

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080)
