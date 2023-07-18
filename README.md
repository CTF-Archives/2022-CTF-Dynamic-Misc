> 引引流（）：https://github.com/CTF-Archives/ctf-docker-template

上次三校联赛出了一些动态Misc，几题考点比较常见，有一题太套了导致零解，果咩那塞

出动态Misc有两个目的，一是纯粹为了好玩，二是为了防止作弊，通常，CTF比赛为选手提供的Misc题目都是静态附件，但是，通过创建一个动态环境，可以在不预先通知选手Misc是动态的情况下将他们套进圈套里（bushi）

![img](https://bfs.iloli.moe/2023/07/5dc74e-b7f356-78805a221a988e79ef3f42d7.png)

### 部署方法

常规部署

```bash
docker build xxx/xxx:xxx .
docker run -d -p [output]:80 xxx/xxx:xxx
```

### MISC1

> 非常非常非常常见的考点，灵感来源于VNCTF东奥那一场，只不过题目是变成了动态的，目录结构如下
>
> 出题人：IceCliffs
>
> 题目名称：Pixels In Picture
>
> 预估难度：**简单-易**
>
> 出题时间：2022/10/11

![img](https://bfs.iloli.moe/2023/07/8827fa-f630b2-78805a221a988e79ef3f42d7.png)

![img](https://bfs.iloli.moe/2023/07/566c02-f457df-78805a221a988e79ef3f42d7.png)

Dockerfile内容十分简单，就常规部署，然后暴露了一个 **80:WEB** 端口而已

```dockerfile
FROM python:3.9-slim
WORKDIR /
COPY app/* /
RUN pip install --upgrade pip setuptools
RUN pip install -r /requirements.txt
COPY main.py main.py
COPY run.sh /
RUN chmod 777 /run.sh
ENTRYPOINT ["/run.sh"]
EXPOSE 80
```

最核心的文件就是 main.py，使用Python是迫不得已的（太jb灵活了主要是），思路很简单，核心就用到了Pillow这个库，然后把flag写进**backJpeg.jpg**，最后把**backJpeg.jpg**拆分开为一个一个小像素块投射在**hiddenJpeg.jpg**里，最后通过Flask暴露80端口提供附件给选手，~~很好玩，不是吗？~~

```python
# Author: IceCliffs
# Date: 2022/10/19
from flask import Flask, send_from_directory
from PIL import Image, ImageDraw, ImageFont
from hashlib import md5
 
# make Flag File
#testFlag = 'flag{' + md5().hexdigest() + '}'
flag = open('/flag', 'r').read()
img = Image.open('./backJpeg.jpg')
w, h = img.size
imgdraw = ImageDraw.Draw(img)
imgdraw.text((w / 10, h / 3), str(flag), fill='#000000')
print('FLAG: ' + flag)
print('IMG SIZE x: ' + str(w) + ' y: ' + str(h))
img = img.rotate(90, expand = 1)
img.save('./flagJpeg.jpg')
 
# Write the flag in the picture 
flagImg = Image.open('./flagJpeg.jpg')
hiddenImg = Image.open('./hiddenJpeg.jpg')
width = flagImg.size[0]
height = flagImg.size[1]
flagImg = flagImg.convert('RGB')
array = []
for i in range(width):
     for j in range(height):
          r, g, b = flagImg.getpixel((i,j))
          rgb = (r, g, b)
          hiddenImg.putpixel(((i+2) * 19,(j + 62) * 11), rgb)
hiddenImg.save('flag.png')
 
# Start Web Service
app = Flask(__name__)
@app.route('/', methods=['GET'])
def displayFlag():
     return send_from_directory('./','flag.png')
 
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)
```

#### Writeup

这题很简单，一张图片里嵌入了像素块化的另一张图

![](https://bfs.iloli.moe/2023/07/63c6a2-f5a5bd-76e3524f699291983daa4a1e.jpg)

细心的小伙伴可能会发现里边有一块一块的像素点，我们只需要写个小脚本把像素块提取出来即可。

像素块左右和上下距离有间隔，自己比划比划。

```python
from PIL import Image
im=Image.open('./flag.png')
lines=[]
for i in range(4066):
    lines.append(crop((0,i,1944,i+1)))
m=[]
for i in range(len(lines)):
    tmp=[]
    for j in range(0,1944,19):#要事先量一下每个被插入的像素点之间x,y相差多少，这个数据只对上图负责
        tmp.append(lines[i].crop((j,0,j+1,1)))
    m.append(tmp)
target=Image.new('RGB',(200,400))
for i in range(len(m)//11):#同上
    for j in range(len(m[0])):
        target.paste(m[i*11][j],(j,i))
target.save('./1.bmp')
```

Code from -Laffey-

PS：原图在这

![img](https://bfs.iloli.moe/2023/07/5dfd9d-cf5249-78805a221a988e79ef3f42d7.png)

### MISC2

这题，会比较套，考点算比较常见，总体来说还算简单，就是套了点

> 出题人：IceCliffs
>
> 题目名称：**わくわく**
>
> 预估难度：**简单-中**
>
> 出题时间：2022/10/11

Dockerfile

```dockerfile
FROM python:3.7-slim
WORKDIR /
COPY app/* /
RUN pip install --upgrade pip setuptools
RUN apt-get update && apt-get install zip vim inetutils-ping -y
RUN pip install -r /requirements.txt
COPY main.py main.py
COPY run.sh /
RUN chmod 777 /run.sh
ENTRYPOINT ["/run.sh"]
EXPOSE 8080
```

大致思路就是直接写hex数据到wav里，然后简简单单频域隐写，最后把他们缝合起来就行了，自己瞎jb写的脚本

```python
# Author: IceCliffs
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

sampling_freq, audio = wavfile.read("flag.wav")

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
write('/flag.wav', sampling_freq, audio_sca)
sampling_freq, audio = wavfile.read("/flag.wav")
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
```

#### Writeup

根据网络上的各种资料可以得知WAVE文件本质上就是一种RIFF格式，它可以抽象成一颗树（数据结构的一种）来看。

![img](https://bfs.iloli.moe/2023/07/1e748b-eef8c7-78805a221a988e79ef3f42d7.png)

我们看到这张图上面，从上到下分别对应着二进制数据在文件中相对于起始位置的偏移量。每一个格子对应一个字段，field size表示每个字段所占据的大小，根据这个大小以及当前的偏移量，我们也可以计算出下一个字段的起始地址（偏移量）。 WAV 是Microsoft开发的一种音频文件格式，它符合上面提到的RIFF文件格式标准，可以看作是RIFF文件的一个具体实例。既然WAV符合RIFF规范，其基本的组成单元也是chunk。一个WAV文件通常有三个chunk以及一个可选chunk，其在文件中的排列方式依次是：RIFF chunk，Format chunk，Fact chunk（附加块，可选），Data chunk…

详见：https://www.cnblogs.com/guojun-junguo/p/10129548.html

**wave.h**

```c
# Author: IceCliffs
# Date: 2022/10/19
#ifndef _EXTRACTDATA_H_
#define _EXTRACTDATA_H_
#include <stdint.h>
typedef struct tagWAVHEADER {
    uint8_t   ChunkID[4];
    uint32_t  ChunkSize;
    uint8_t   Format[4];
    uint8_t   FmtChunkID[4];
    uint32_t  FmtChunkSize;
    uint16_t  AudioFormat;
    uint16_t  NumChannels;
    uint32_t  SampleRate;
    uint32_t  ByteRate;
    uint16_t  BlockAlign;
    uint16_t  BitsPerSample;
    uint8_t   DataChunkID[4];
    uint32_t  DataChunkSize;
} WAVHEADER;
#endif  // #ifndef _EXTRACTDATA_H_
```

具体就是写个脚本跑一下压缩包位置，提出压缩包，题目提示了x10。。是每个字节x10，不是一块的，抱歉。

写个脚本跑一下压缩包的位置

**exp.c**

```c
# Author: IceCliffs
# Date: 2022/10/19
#include<stdio.h>   
#include<stdlib.h>
#include "wave.h"
#define  W  128
int FileSet = 0;
int FileEnd = 0;
int FileLength = 0;
short InputData[W];
WAVHEADER FileHeader;
int main() {
    FILE *wavFile;
    wavFile = fopen("wakuwaku.wav", "rb");
    fseek(wavFile, 0L, SEEK_END);  
    FileEnd = ftell(wavFile);   
    rewind(wavFile);
    long n = 0;
    fread(&FileHeader, 1, sizeof(WAVHEADER), wavFile);
    FileLength = FileEnd / 2;
    while (FileLength >= W) {
        fread(InputData, sizeof(short), W, wavFile);
        for (int i = 0; i < W; i++) {
            if (
                InputData[i] == (int)('5' * 10) && \ 
                InputData[i + 1] == (int)('0' * 10) && \ 
                InputData[i + 2] == (int)('4' * 10) 
            )
            {
                printf("%d\n", n);
            }
            n++;
        }
        FileLength -= W;
    }
    return 0;
}
```

![img](https://bfs.iloli.moe/2023/07/4b78d1-be5f3e-78805a221a988e79ef3f42d7.png)

得到两个压缩包位置，把他们提取出来，提取脚本自己写，具体做法定位往后加几位然后/10就可以了，具体要加多少我不知道，因为是随机的（，包括定位，全是随机的（，但范围在可控之内，所以不用担心做不出来。

第一个压缩包是假的压缩包，位置比较前面。内容如下（意义不明）

**165313**

![img](https://bfs.iloli.moe/2023/07/833116-3ba458-78805a221a988e79ef3f42d7.png)

![img](https://bfs.iloli.moe/2023/07/a113ee-5b835d-78805a221a988e79ef3f42d7.png)

第二个才是真正藏有flag的压缩包，压缩包密码在频谱图那里。

![img](https://bfs.iloli.moe/2023/07/b06b61-65579d-43e1de06126bd45172771c75.jpg)

**1859051**

Cipher: i1@mn!s*(e

![img](https://bfs.iloli.moe/2023/07/3cfc87-d7e7ef-78805a221a988e79ef3f42d7.png)

最后输入压缩包密码解压得到flag

![img](https://bfs.iloli.moe/2023/07/6f2c73-c0e8c9-78805a221a988e79ef3f42d7.png)

![img](https://bfs.iloli.moe/2023/07/8b4fa9-c90517-78805a221a988e79ef3f42d7.png)

**flag{4bd390e9-78f8-4567-9204-1cf7477891de}**

很常见的音频考点，挺简单的，真的