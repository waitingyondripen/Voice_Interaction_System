import pyaudio,wave
import numpy as np
from voice_awakening import wakeup
from playsound import playsound

# 该文件实现的功能是自适应语音录制模块，在模块中设置了mindb这一参数，当麦克风检测到声音大于6000时，开始录音。
# 若在录音过程中，开始录音后，声音小于mindb，则记录该时刻，若在随后delayTime的时间内仍小于mindb，则停止录音
# 由此实现自适应语音录制的功能

def listen():
    temp = 20
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 2
    WAVE_OUTPUT_FILENAME = './wav_file/hear.wav'


    mindb=6000    #最小声音，大于则开始录音，否则结束，可调整
    delayTime=2.0  #小声2.0秒后自动终止，可调整
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    #snowboydecoder.play_audio_file()
    print("开始!计时")

    frames = []
    flag = False            # 开始录音节点
    stat = True				#判断是否继续录音
    stat2 = False			#判断声音小了

    tempnum = 0				#tempnum、tempnum2、tempnum3为时间
    tempnum2 = 0


    while stat:
        data = stream.read(CHUNK,exception_on_overflow = False)
        frames.append(data)
        audio_data = np.frombuffer(data, dtype=np.short)
        temp = np.max(audio_data)
        if(tempnum > 50 and tempnum2 == 0):
            print("等待唤醒......")
            stream.stop_stream()
            wakeup()
            playsound('./wav_file/welcome.wav')
            print("  ")
            print("唤醒成功！")
            stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
            tempnum = 0
        if temp > mindb and flag==False:
            flag =True
            print("开始录音")
            tempnum2=tempnum

        if flag:

            if(temp < mindb and stat2==False):
                stat2 = True
                tempnum2 = tempnum
                print("声音小，且之前是是大的或刚开始，记录当前点")
            if(temp > mindb):
                stat2 =False
                tempnum2 = tempnum
                #刷新

            if(tempnum > tempnum2 + delayTime*15 and stat2==True):
                print("间隔%.2lfs后开始检测是否还是小声"%delayTime)
                if(stat2 and temp < mindb):
                    stat = False
                    #还是小声，则stat=True
                    print("小声！")
                else:
                    stat2 = False
                    print("大声！")


        print(str(temp)  +  "      " +  str(tempnum))
        tempnum = tempnum + 1
        if tempnum > 500:				#超时直接退出
            stat = False
    print("录音结束")

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
