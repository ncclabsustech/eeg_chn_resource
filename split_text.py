import re


def __merge_symmetry(sentences, symmetry=('“', '”')):
    """把双引号中的内容全放一个元素里"""

    effective_ = []

    merged = True

    for index in range(len(sentences)):

        if symmetry[0] in sentences[index] and symmetry[1] not in sentences[index]:

            merged = False

            effective_.append(sentences[index])

        elif symmetry[1] in sentences[index] and not merged:

            merged = True

            effective_[-1] += sentences[index]

        elif symmetry[0] not in sentences[index] and symmetry[1] not in sentences[index] and not merged:

            effective_[-1] += sentences[index]

        else:

            effective_.append(sentences[index])

    return [i.strip() for i in effective_ if len(i.strip()) > 0]


def __merge_symmetry2list(sentences, symmetry=('“', '”')):
    """把引号中的内容放进一个列表里（如果有多句话），只有一句的话就不放"""

    effective_ = []
    quotation = []

    merged = True

    for index in range(len(sentences)):
        sentences[index] = sentences[index].replace("\n", "")

        if symmetry[0] in sentences[index] and symmetry[1] not in sentences[index]:

            merged = False

            # effective_.append(sentences[index])
            quotation.append(sentences[index])

        elif symmetry[1] in sentences[index] and not merged:

            merged = True

            quotation.append(sentences[index])
            effective_.append(quotation.copy())
            quotation.clear()

        elif symmetry[0] not in sentences[index] and symmetry[1] not in sentences[index] and not merged:

            quotation.append(sentences[index])

        else:

            effective_.append(sentences[index])

    return effective_


def to_sentences(paragraph):
    """由段落切分成句子"""

    sentences = re.split(r"(？|。|！|\…\…|：)", paragraph)

    sentences.append("")

    sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]

    sentences = [i.strip() for i in sentences if len(i.strip()) > 0]

    for j in range(1, len(sentences)):

        if sentences[j][0] == '”':
            sentences[j - 1] = sentences[j - 1] + '”'

            sentences[j] = sentences[j][1:]

    return __merge_symmetry2list(sentences)
    # return sentences

"""
1.引号内不分：用__merge_symmetry
2.引号内分：都不用
3.引号内分，放列表：__merge_symmetry2list
"""


filename = "xiaowangzi_zhoukexi_main_text.txt"
with open(filename, 'r', encoding='utf-8') as file:
    text = file.read()

    result = to_sentences(text)
    # print(result)

    for e in result:
        print(e)
