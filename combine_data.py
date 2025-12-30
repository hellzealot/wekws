import os
import struct
import numpy as np

def combine_dat_files_range(start=0, end=10,dir = "", prefix="input_", 
                           output_txt="input_combine.txt", 
                           output_bin="input_combine.bin"):
    """
    合并指定范围内的.dat文件
    输出两种格式：
    1. 文本格式（每行一个文件）
    2. 二进制格式（连续存储，无分隔符）
    """
    all_data = []  # 存储所有数据
    valid_file_count = 0
    
    # 首先读取所有数据
    for i in range(start, end + 1):
        filename = dir + f"{prefix}{i}.txt"
        if os.path.exists(filename):
            with open(filename, 'r') as in_f:
                content = in_f.read().strip()
                if content:  # 确保内容非空
                    # 将字符串转换为浮点数列表
                    try:
                        numbers = [float(x) for x in content.split()]
                        all_data.append(numbers)
                        valid_file_count += 1
                        if valid_file_count % 100 == 0 and valid_file_count > 0:
                            print(f"已处理{valid_file_count}个文件")
                    except ValueError as e:
                        print(f"警告: 文件 {filename} 包含非浮点数数据: {e}")
                else:
                    print(f"警告: 文件 {filename} 为空，已跳过")
        else:
            print(f"警告: 文件 {filename} 不存在，已跳过")
    
    if valid_file_count == 0:
        print("错误: 没有找到有效文件")
        return
    
    # 1. 输出文本格式
    with open(output_txt, 'w') as out_txt:
        for numbers in all_data:
            # 将浮点数列表转换回字符串
            line = ' '.join(str(x) for x in numbers)
            out_txt.write(line + '\n')
    
    # 2. 输出二进制格式
    with open(output_bin, 'wb') as out_bin:
        for numbers in all_data:
            # 将每个浮点数转换为二进制（双精度浮点数，8字节）
            for num in numbers:
                # 使用 struct 打包为二进制
                out_bin.write(struct.pack('f', num))  # 'f' 表示单精度浮点数'
    
    print(f"合并完成！")
    print(f"成功处理: {valid_file_count} 个文件")
    print(f"文本格式输出: {output_txt}")
    print(f"二进制格式输出: {output_bin}")
    print(f"二进制文件大小: {os.path.getsize(output_bin)} 字节")


if __name__ == '__main__':
    combine_dat_files_range(1,3787,"/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/dump/",
                            "input_","/home/hlj/wekws/featuremap/input_combine.txt","/home/hlj/wekws/featuremap/input_combine.bin")
    
    combine_dat_files_range(1,3787,"/home/hlj/wekws/wekws/examples/hi_xiaowen/s0/dump/",
                            "input_cache_","/home/hlj/wekws/featuremap/input_cache_combine.txt","/home/hlj/wekws/featuremap/input_cache_combine.bin")