import re
import jieba
import numpy as np
import argparse

"""递归调用，检查句子长度，超过某长度按逗号分"""

newline = "<sep>"


# todo: overload,测试英文

def to_sentences(paragraph, mode, language):
    """由段落切分成句子
    @:param paragraph: str文本
    @:param mode:按什么切分，三种："quotation_mark"、"full_stop"、"comma"
            "quotation_mark"表示按引号切分，"full_stop"表示按句末符号（句号、问号、叹号等）切分、"comma"表示按逗号切分
    """

    marks_ch = ["？", "。", "！", "\…\…", "：", "，"]
    marks_en = ["?", ".", "!", "\…", ":", ","]

    if language == "Chinese":

        if mode == "quotation_mark":
            sentences = re.split(r"(“|”)", paragraph)
        elif mode == "full_stop":
            sentences = re.split(r"(？|。|！|\…\…|：)", paragraph)
        elif mode == "comma":
            sentences = re.split(r"(，)", paragraph)
        else:
            raise Exception("invalid mode")

    else:
        if mode == "quotation_mark":
            sentences = re.split(r"(\"|\")", paragraph)
        elif mode == "full_stop":
            sentences = re.split(r"(\?|\.|\!|\…|:)", paragraph)
        elif mode == "comma":
            sentences = re.split(r"(,)", paragraph)
        else:
            raise Exception("invalid mode")

    sentences.append("")

    sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]

    sentences = [i.strip().replace("\n", "") for i in sentences if len(i.strip()) > 0]

    if language == "Chinese":

        for j in range(len(sentences) - 1):
            if sentences[j][-1] == '“':
                sentences[j + 1] = "“" + sentences[j + 1]
                sentences[j] = sentences[j][:-1]

            if sentences[j + 1][0] in marks_ch:
                sentences[j] = sentences[j] + sentences[j + 1][0]
                sentences[j + 1] = sentences[j + 1][1:]

            if sentences[j + 1][0] == '”':
                sentences[j] = sentences[j] + "”"
                sentences[j + 1] = ""

    else:
        for j in range(len(sentences) - 1):
            if sentences[j][-1] == '"':
                sentences[j + 1] = "\"" + sentences[j + 1]
                sentences[j] = sentences[j][:-1]

            if sentences[j + 1][0] in marks_ch:
                sentences[j] = sentences[j] + sentences[j + 1][0]
                sentences[j + 1] = sentences[j + 1][1:]

            if sentences[j + 1][0] == '"':
                sentences[j] = sentences[j] + '"'
                sentences[j + 1] = ""

    sentences = list(filter(lambda x: x != '', sentences))

    for i in range(len(sentences)):
        if mode == "quotation_mark":
            sentences[i] = to_sentences(sentences[i], mode="full_stop", language=language)

    if mode == "full_stop":
        for i in range(len(sentences)):

            # if len(sentences[i]) > 10 and ("，" in sentences[i] or "," in sentences[i]):
            sentences[i] = to_sentences(sentences[i], mode="comma", language=language)
            for idx in range(len(sentences[i])):
                sentences[i][idx] = str2dict(sentences[i][idx], language=language)

    return sentences


def str2dict(text, language):
    """
    :param text: str
    :return: dict，包含两个field：text--原文本，index--原文本经过分词后得到的index，其中1表示词尾，0为非词尾
    例子：'text': '蟒蛇把猎物囫囵吞下，', 对应的分词结果为'蟒蛇|把|猎物|囫囵|吞|下|，|' 对应的'index': array([0., 1., 1., 0., 1., 0., 1., 0., 1., 1.])}
    """
    if language == "Chinese":
        result = jieba.cut(text, cut_all=False)
    else:
        result = re.findall(r"\w+|[.]", text)

    index = np.zeros(len(text))
    count = 0

    # 切分处为1
    for element in result:
        for i in range(len(element)):
            if i == len(element) - 1:
                index[count] = 1
            count += 1

    dictionary = {"text": text, "index": index}

    return dictionary


def split(file_path, language):
    """
    :param file_path: 文件路径
    :param language: 文件对应的语言,"Chinese" or "English"
    :return: list，每个元素是分词后的dict

    用来调用to_sentences的

    """
    if language == "Chinese" or "English":

        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            result = to_sentences(text, mode="quotation_mark", language=language)
            return result
    else:
        raise Exception("invalid language")

def main():
    # parser = argparse.ArgumentParser()
    #
    # # 添加命令行选项
    # parser.add_argument("-f", "--file", help="指定文件路径")
    # parser.add_argument("-l", "--language", help="指定文本语言")
    #
    # # 解析命令行参数
    # args = parser.parse_args()
    #
    # # 获取选项的值
    # file_path = args.file
    # language = args.language

    filename = "xiaowangzi_zhoukexi_main_text.txt"

    result = split(filename, language="Chinese")

    for e in result:
        print(e)


if __name__ == "__main__":
    main()
