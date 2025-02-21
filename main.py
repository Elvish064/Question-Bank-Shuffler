import os
import argparse
import random
import chardet

def detect_encoding(file_path):
    """检测文件编码格式"""
    with open(file_path, "rb") as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result["encoding"]

def convert_to_utf8(input_file):
    """自动转换文件编码为 UTF-8"""
    original_encoding = detect_encoding(input_file)

    if original_encoding.lower() != "utf-8":
        print(f"已将文档由 {original_encoding} 转化为 UTF-8 并进行操作。")
        utf8_file = input_file + ".utf8"

        with open(input_file, "r", encoding=original_encoding, errors="ignore") as f:
            content = f.read()

        with open(utf8_file, "w", encoding="utf-8") as f:
            f.write(content)

        return utf8_file
    return input_file

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="随机打乱题库选项，并生成对应答案文件。\n This project is openspurce on GitHub: https://github.com/Elvish064/Question-Bank-Shuffler")
    parser.add_argument("-i", "--input", required=True, help="原始题库 txt 文件路径[Required]")
    parser.add_argument("-o", "--output", help="处理后题库的输出路径[Optional]")
    parser.add_argument("-a", "--answer", help="答案文件路径[Optional]")

    args = parser.parse_args()

    if not args.input:
        print("没有输入原题库 txt 路径")
        exit(1)

    # 转换为 UTF-8 编码
    utf8_input = convert_to_utf8(args.input)

    # 获取输入文件名（不带路径和扩展名）
    input_filename = os.path.basename(args.input)
    filename_no_ext = os.path.splitext(input_filename)[0]

    # 生成默认输出目录
    output_dir = os.path.join(os.path.dirname(args.input), "output")
    os.makedirs(output_dir, exist_ok=True)

    # 设置默认输出文件路径
    if not args.output:
        args.output = os.path.join(output_dir, f"output_{filename_no_ext}.txt")

    if not args.answer:
        args.answer = os.path.join(output_dir, f"answer_{filename_no_ext}.txt")

    return args, utf8_input

def read_questions(file_path):
    """读取题库文件（UTF-8 编码）并按块分割题目"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    blocks = []
    current_block = []

    for line in content.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("[I]") and current_block:
            blocks.append(current_block)
            current_block = []
        current_block.append(line)

    if current_block:
        blocks.append(current_block)

    return blocks

def process_blocks(blocks):
    """处理每个题目块，添加题号，打乱选项顺序，并记录答案"""
    answer_key = []
    processed_blocks = []
    
    for idx, block in enumerate(blocks, start=1):
        question_id = None
        options_content = []
        original_answer = None
        
        # 第一遍扫描：获取题目 ID 和选项内容（同时记录[A]的原答案）
        for i, line in enumerate(block):
            if line.startswith("[I]"):
                question_id = line.split("]")[1].strip()
                block[i] = f"[I]{idx}.{question_id}"  # 添加题号
            elif line.startswith("[A]"):
                original_answer = line[3:].strip()
                options_content.append(original_answer)
            elif line.startswith("[B]") or line.startswith("[C]") or line.startswith("[D]"):
                options_content.append(line[3:].strip())

        # 如果选项数量不等于4，则不进行打乱
        if len(options_content) != 4:
            processed_blocks.append(block)
            if question_id:
                answer_key.append(f"{idx}.{question_id}: A")
            continue
        
        # 打乱选项内容
        random.shuffle(options_content)
        
        # 确定正确答案的新位置
        try:
            correct_index = options_content.index(original_answer)
        except ValueError:
            correct_index = 0
        correct_letter = chr(ord("A") + correct_index)
        
        if question_id:
            answer_key.append(f"{idx}.{question_id}: {correct_letter}")
        
        # 生成新的选项行
        new_options = [
            f"[A]{options_content[0]}",
            f"[B]{options_content[1]}",
            f"[C]{options_content[2]}",
            f"[D]{options_content[3]}"
        ]
        
        # 第二遍扫描：遍历原题目块，遇到选项行时依次替换为打乱后的新选项，其他行保持不变
        new_block = []
        option_index = 0
        for line in block:
            if line.startswith("[A]") or line.startswith("[B]") or line.startswith("[C]") or line.startswith("[D]"):
                new_block.append(new_options[option_index])
                option_index += 1
            else:
                new_block.append(line)
        
        processed_blocks.append(new_block)
    
    return processed_blocks, answer_key

def write_output(file_path, blocks):
    """写入打乱后的题库（UTF-8 编码）"""
    with open(file_path, "w", encoding="utf-8") as f:
        for block in blocks:
            f.write("\n".join(block) + "\n\n")

def write_answers(file_path, answers):
    """写入答案文件（UTF-8 编码）"""
    with open(file_path, "w", encoding="utf-8") as f:
        for ans in answers:
            f.write(ans + "\n")

def main():
    args, utf8_input = parse_args()

    # 读取原题库
    blocks = read_questions(utf8_input)

    # 处理题库
    processed_blocks, answer_key = process_blocks(blocks)

    # 写入文件
    write_output(args.output, processed_blocks)
    write_answers(args.answer, answer_key)

    print(f"处理完成！\n题库输出文件: {args.output}\n答案文件: {args.answer}")

    # 清理临时转换的 UTF-8 文件
    if utf8_input.endswith(".utf8"):
        os.remove(utf8_input)

if __name__ == "__main__":
    main()
