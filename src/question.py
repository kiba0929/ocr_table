#Indexに対して質問するメソッドを追加
import make_index as Index
def question_to_translated(indexes_translated,q):
  for i in range(Index.num_docx):
    question_translated = Index.translator.translate_text(q,source_lang="JA",target_lang="EN-US",glossary=mydic_id_ja_en)
    answer_en = indexes_translated[i].query(question_translated.text)
    answer_ja = Index.translator.translate_text(str(answer_en),source_lang="EN",target_lang="JA",glossary=mydic_id_en_ja)
    print(i)
    print(answer_ja.text)
    if(i!=Index.num_docx-1):print("---")

def question_to_japanese(indexes,q):
  for i in range(Index.num_docx):
    answer = indexes[i].query(q)
    print(i)
    print(answer)
    if(i!=Index.num_docx-1):print("---")