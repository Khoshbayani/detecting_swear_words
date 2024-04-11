import hazm
from hazm import word_tokenize
import numpy as np
from ordered_set import OrderedSet
import string

normalizer = hazm.Normalizer()


def replaceDoubleCharacters(string):
    lastLetter, replacedString = "", ""
    for letter in string:
        if letter != lastLetter:
            replacedString += letter
        lastLetter = letter
    return replacedString


# کلمات رکیک موجود در دیتابیس

with open("data (1).txt",encoding='utf-8') as f:
    swear_words = set()
    for s in f.read().split('\n'):
        swear_words.add(normalizer.normalize(s))



with open("whitelist_nonenormalized_allcombined.txt",encoding='utf-8') as f:
    whitetext =  f.read()
    whitetext=whitetext+ " " +normalizer.normalize(whitetext)



def jaccard_similarity(word1, word2):
    set1 = set(word1)
    set2 = set(word2)
    return len(set1.intersection(set2)) / len(set1.union(set2))





def detect_swearwords_from_text(input_text, threshold1=0.5,threshold2=0.65):
    if input_text == None:
        raise ValueError("مقدار text را وارد نمایید")
    warning = ""
    input_text= replaceDoubleCharacters(input_text)


    for punc in list(string.punctuation+"؟،؛"+"ـ"):
        if punc in input_text:
            input_text = input_text.replace(punc , " ")
    else:
        input_text = hazm.Normalizer().normalize(input_text)


    tokens= word_tokenize(input_text)

    number_of_one_char = 0
    number_of_two_char = 0

    index_of_fist_fragment = -1
    index_of_last_fragment = -1
    for i in range(len(tokens)):
        t = tokens[i]
        if len(t) == 1:
            if not t.isdigit():
                number_of_one_char += 1
                if index_of_fist_fragment == -1:
                    index_of_fist_fragment = i
                else:
                    index_of_last_fragment = i

        elif len(t) == 2:
            if whitetext.find(f" {t} ") == -1:
                if not t.isdigit():
                    number_of_two_char += 1
                    if index_of_fist_fragment == -1:
                        index_of_fist_fragment = i
                    else:
                        index_of_last_fragment = i


    if ((number_of_one_char * 2)+(number_of_two_char)) >= 4:
        # frgmnt = "".join(tokens[index_of_fist_fragment:index_of_last_fragment+1])

        warning = "مشکوک به منقطع نویسی!"


        # tokens1 = tokens[:index_of_fist_fragment]
        # tokens2 = tokens[index_of_last_fragment+1:]
        #
        # tokens1.append(frgmnt)
        #
        # tokens1.extend(tokens2)
        # tokens = tokens1

    # temp_tok2 = []
    # if len(tokens) >=2 :
    #     for i in range(len(tokens)):
    #         if (i + 2) <= len(tokens):
    #             temp_new_phrase = " ".join(tokens[i:i+2])
    #             temp_tok2.append(temp_new_phrase)
    #
    #
    #
    # temp_tok3 = []
    # if len(tokens) >=3 :
    #     for i in range(len(tokens)):
    #         if (i + 3) <= len(tokens):
    #             temp_new_phrase = " ".join(tokens[i:i+3])
    #             temp_tok3.append(temp_new_phrase)
    #
    #
    #
    #
    # temp_tok4 = []
    # if len(tokens) >=4 :
    #     for i in range(len(tokens)):
    #         if (i + 4) <= len(tokens):
    #             temp_new_phrase = " ".join(tokens[i:i+4])
    #             temp_tok4.append(temp_new_phrase)
    #
    #
    #
    # temp_tok5 = []
    # if len(tokens) >=5 :
    #     for i in range(len(tokens)):
    #         if (i + 5) <= len(tokens):
    #             temp_new_phrase = " ".join(tokens[i:i+5])
    #             temp_tok5.append(temp_new_phrase)

    temp_tok = []
    if len(tokens) >= 2 :
        for lt in range(2,len(tokens)):
            for i in range(len(tokens)):
                if (i + lt) <= len(tokens):
                    temp_new_phrase = " ".join(tokens[i:i+lt])
                    temp_tok.append(temp_new_phrase)
        else:
            tokens.extend(temp_tok)


    # tokens.extend(temp_tok2)
    # tokens.extend(temp_tok3)
    # tokens.extend(temp_tok4)
    # tokens.extend(temp_tok5)
    # tokens.extend(temp_tok6)

    tokens = list(OrderedSet(tokens))

    try:
        tokens.remove("")
    except:
        pass





    result =[]
    for t in tokens:
        if len(t)>=1 and whitetext.find(f" {str(t)} ") == -1 :
            for sw in swear_words:
                sim = jaccard_similarity(t,sw)

                if sim>threshold1:

                    t_set = OrderedSet(list(t))
                    sw_set = OrderedSet(list(sw))
                    list_of_jaccard_value = []
                    for t_alph in t_set:
                        index_of_t_alph = np.where(np.asarray(t_set) == t_alph)[0][0]
                        pre_t = t_set[:index_of_t_alph]
                        post_t = t_set[index_of_t_alph+1:]

                        try:
                            index_of_bl_alph = np.where(np.asarray(sw_set) == t_alph)[0][0]
                        except:
                            pass
                        else:
                            pre_bl = sw_set[:index_of_bl_alph]
                            post_bl = sw_set[index_of_bl_alph+1:]

                            if len(pre_t) >0 and len(pre_bl) >0:
                                jc_value = jaccard_similarity(pre_t,pre_bl)
                                list_of_jaccard_value.append(jc_value)



                            if len(post_t) >0 and len(post_bl) >0:
                                jc_value = jaccard_similarity(post_t , post_bl)
                                list_of_jaccard_value.append(jc_value)

                    else:
                        seq_mactch = sum(list_of_jaccard_value) / len(list_of_jaccard_value)
                    if seq_mactch > threshold2:
                        result.append({"in-blacklist":sw,"in-givenText":t,"sim-value":str(int(sim*100))})


    return (result , warning)
