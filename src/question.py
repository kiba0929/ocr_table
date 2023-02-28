#Indexに対して質問するメソッドを追加
import make_index as Index
import logging

#logの設定
logger = logging.getLogger('mylog')

def question_to_translated(indexes_translated,q):
  for i in range(Index.num_docx):
    question_translated = Index.translator.translate_text(q,source_lang="JA",target_lang="EN-US",glossary=Index.mydic_id_ja_en)
    answer_en = indexes_translated[i].query(question_translated.text)
    answer_ja = Index.translator.translate_text(str(answer_en),source_lang="EN",target_lang="JA",glossary=Index.mydic_id_en_ja)
    logger.info(f"{i+1}人目")
    logger.info(answer_ja.text)
    if(i!=Index.num_docx-1):logger.info("---")

def question_to_japanese(indexes_ja,q):
  for i in range(Index.num_docx):
    answer = indexes_ja[i].query(q)
    logger.info(f"{i+1}人目")
    logger.info(answer)
    if(i!=Index.num_docx-1):logger.info("---")