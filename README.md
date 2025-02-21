# Question-Bank-Shuffler
A script to shuffle questions and generate answer files automatically for 中国业余电台操作证书考试题库

> [!NOTE]
> 本项目仅适用于 中国业余电台操作证书考试题库
> 但是如果有其它形如这样的题库，那么也适用：
```
[I]LK0001
[Q]<Question>：
[A]<Answer1>
[B]<Answer2>
[C]<Answer3>
[D]<Answer4>
[P]

[I]LK0002
[Q]<Question>：
[A]<Answer1>
[B]<Answer2>
[C]<Answer3>
[D]<Answer4>
[P]
...
```
---
## ⭐Features
- Automatically detects and converts non-UTF-8 files (e.g., GBK) to UTF-8
- Renumbers questions
- Randomly shuffles answer choices
- Outputs a shuffled question bank and corresponding answer file

## ⬇️Installation
```bash
git clone https://github.com/your-username/question-bank-shuffler.git
cd question-bank-shuffler
pip install -r requirements.txt
```

## 📑Usage
```
python main.py -h
usage: main.py [-h] -i INPUT [-o OUTPUT] [-a ANSWER]

随机打乱题库选项，并生成对应答案文件。

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        原始题库 txt 文件路径[Required]
  -o OUTPUT, --output OUTPUT
                        处理后题库的输出路径[Optional]
  -a ANSWER, --answer ANSWER
                        答案文件路径[Optional]

Example:python main.py -i sample_questions.txt -o shuffled_questions.txt -a answers.txt

```

## ✅License
MIT License