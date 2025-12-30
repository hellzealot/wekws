#!/home/hlj/anaconda3/envs/wekws/bin/python
import sys
import os
import torch
import torch.distributed as dist

# 添加实际的wekws路径到Python路径
wekws_path = "/home/hlj/wekws/wekws"
if wekws_path not in sys.path:
    sys.path.insert(0, wekws_path)

def setup_distributed():
    """模拟torchrun的分布式环境"""
    # 设置环境变量
    os.environ['RANK'] = '0'
    os.environ['LOCAL_RANK'] = '0'
    os.environ['WORLD_SIZE'] = '1'
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '29500'
    
    # 初始化进程组（单机模式）
    if not dist.is_initialized():
        dist.init_process_group(
            backend='nccl' if torch.cuda.is_available() else 'gloo',
            init_method='env://',
            world_size=1,
            rank=0
        )

if __name__ == "__main__":
    # 设置分布式环境
    setup_distributed()
    
    # 现在导入并运行训练脚本
    from wekws.bin.train import main
    
    # sys.argv = [
    #     "train.py",
    #     "--gpus", "0",
    #     "--config", "conf/fsmn_ctc.yaml",
    #     #"--train_data", "data/train/data.list",
    #     #"--cv_data", "data/dev/data.list",
    #     "--train_data", "/mnt/h/GigaSpeechV1/KWS/train.list",
    #     "--cv_data", "/mnt/h/GigaSpeechV1/KWS/dev.list",
    #     "--model_dir", "exp/fsmn_ctc",
    #     "--num_workers", "2",
    #     "--num_keywords", "2599",
    #     "--min_duration", "50",
    #     "--seed", "666",
    #     "--cmvn_file", "/mnt/h/GigaSpeechV1/KWS/global_cmvn.kaldi",
    #     "--norm_var",
    #     #"--checkpoint", "speech_charctc_kws_phone-xiaoyun/train/base.pt"
    # ]

    # sys.argv = [
    #     "train.py",
    #     "--gpus", "0",
    #     "--config", "conf/fsmn_ctc_adv.yaml",
    #     "--train_data", "/mnt/h/GigaSpeechV1/KWS/train.list",
    #     "--cv_data", "/mnt/h/GigaSpeechV1/KWS/dev.list",
    #     "--model_dir", "/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/modelzoo/fsmn_adv",
    #     "--num_workers", "2",
    #     "--num_keywords", "71",
    #     "--min_duration", "50",
    #     "--seed", "666",
    #     "--cmvn_file", "/mnt/h/GigaSpeechV1/KWS/global_cmvn.kaldi",
    #     "--norm_var",
    #     #"--checkpoint", "/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/modelzoo/fsmn_ctc_12/23.pt"
    # ]

    sys.argv = [
        "train.py",
        "--gpus", "0",
        "--config", "conf/fsmn_ctc8_adv.yaml",
        "--train_data", "/mnt/h/MAGICDATA/train.json",
        "--cv_data", "/mnt/h/MAGICDATA/test.json",
        "--model_dir", "/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/modelzoo/fsmn8_adv_cn",
        "--dict","/mnt/h/MAGICDATA",
        "--num_workers", "2",
        "--num_keywords", "1214",
        "--min_duration", "50",
        "--seed", "666",
        "--cmvn_file", "/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/data/global_cmvn.kaldi",
        "--norm_var",
        #"--checkpoint", "/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/modelzoo/fsmn_adv_cn/6.pt"
    ]
    
    try:
        main()
    finally:
        # 清理分布式环境
        if dist.is_initialized():
            dist.destroy_process_group()
