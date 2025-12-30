#!/home/hlj/anaconda3/envs/wekws/bin/python
import sys
import os
import torch
import torch.distributed as dist

# 添加实际的wekws路径到Python路径
wekws_path = "/home/hlj/wekws/wekws"
if wekws_path not in sys.path:
    sys.path.insert(0, wekws_path)

wekws_tools_path = "/home/hlj/wekws/wekws/tools"
if wekws_tools_path not in sys.path:
    sys.path.insert(0, wekws_tools_path)

if __name__ == "__main__":
    
    # 现在导入并运行训练脚本
    from wekws.bin.stream_kws_ctc import demo
    
    # fsmn_ctc_8的55.pt目前最好，准确率45%

    # sys.argv = [
    #     "stream_kws_ctc.py",
    #     "--config", "/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/modelzoo/fsmn_ctc_12/config.yaml", 
    #     "--checkpoint", "/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/modelzoo/fsmn_ctc_12/150.pt", 
    #     #"--wav_path", "/mnt/h/GigaSpeechV1/KWS/takephoto.wav",
    #     "--wav_path", "/mnt/e/AudioCode/all/Malaysian/142_M/142_M_Fast_1.wav",
    #     #"--wav_path", "/mnt/h/GigaSpeechV1/KWS/test/fe/fe1e52d4340c5c9966cc6e6a613e8141.wav",
    #     "--keywords","T,EY1,K,F,OW1,T,OW2",
    #     "--token_file","/mnt/h/GigaSpeechV1/KWS/tokens.txt",
    #     #"--keywords","我要拍照",
    #     #"--token_file","/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/mobvoi_kws_transcription/tokens.txt",
    #     "--lexicon_file","/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/mobvoi_kws_transcription/lexicon.txt"
    # ]

    #test_full.wav 内容：
    # 0S - 5S ： 当前存储卡性能差，可能导致视频缺失，建议更换 5S - 7S ： 后路镜头未连接 14S - 16S : 后路镜头未连接 25S - 27S : 后路镜头未连接
    # 29S-31S ： 我要拍照 35S-37S ： 打开空调 42S-44S ： take a picture 46S-47S： take a photo 51S-52S：take photo
    
    sys.argv = [
        "stream_kws_ctc.py",
        "--config", "/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/modelzoo/fsmn8_adv_cn/config.yaml", 
        "--checkpoint", "/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/modelzoo/fsmn8_adv_cn/118.pt", 
        #"--wav_path", "/mnt/h/MAGICDATA/woyaopaizhao.wav",
        "--wav_path", "/mnt/d/Board/audio/test_full.wav",
        #"--wav_path", "/mnt/e/AudioCode/In_Vehicle_Noise_Dataset/Segments/cn/29717fd2a6dc2c3e77e4f7c729552975.wav",  #噪音
        "--keywords","T,EY1,K,F,OW1,T,OW2",
        "--token_file","/mnt/h/MAGICDATA/vocab.txt",
        #"--keywords","我要拍照",
        #"--token_file","/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/mobvoi_kws_transcription/tokens.txt",
        "--lexicon_file","/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/mobvoi_kws_transcription/lexicon.txt"
    ]
    
    demo()

