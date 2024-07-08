from paddlespeech.server.bin.paddlespeech_client import ASROnlineClientExecutor
from paddlespeech.server.bin.paddlespeech_client import TextClientExecutor
from paddlespeech.server.bin.paddlespeech_client import TTSOnlineClientExecutor
from voice_awakening import wakeup
from ASR import asr
from record_voice import listen
from playsound import playsound
from deepseek import deepseek

def voice_procedure():
    #关键词唤醒
    print("等待唤醒......")
    wakeup()
    playsound('./wav_file/welcome.wav')
    print("  ")
    print("唤醒成功！")

    messages = []
    #可更改初始化控制需求，即赋予大模型一个规则，每次回答都要遵循该规则
    messages.append({'role': 'system', 'content': "请以情感智能助手的身份简要回答问题,尽量控制在一百字之内"}) 

    try:
        while(1) :
            
            #自适应语音录制
            listen()

            #语音转文本
            input_text = asr.asr()
            print("input text is: ", input_text)

            #大模型回答
            messages.append({'role': 'user', 'content': input_text})

            response = deepseek(messages)

            messages.append({'role': 'assistant', 'content': response})

            #语音合成
            executor = TTSOnlineClientExecutor()
            executor(
                input=response,
                server_ip="127.0.0.1",
                port=8092,
                protocol="http",
                spk_id=1,
                output=None,
                play=True)
            
    except KeyboardInterrupt:
        print('Stopping ...')

        
if __name__=="__main__":
    voice_procedure()