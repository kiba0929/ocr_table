#日本語でのIndexと英語でのIndexをメソッド分けて作成する、共通処理は共通化
import os
from os.path import join,dirname
from dotenv import load_dotenv
import docx2txt
from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor
from gpt_index.indices.prompt_helper import PromptHelper
import deepl

num_docx = 2

def set_env():
  dotenv_path = join(dirname(__file__), '.env')
  load_dotenv(dotenv_path)

def process_docx():
  for i in range(num_docx):
    filename = f'{i+1}'
    print(filename)
    text = docx2txt.process(f'data/data_docx/{filename}.docx')

    # GPT Index の仕様上、区切り文字は半角スペースである必要がある
    text = ' ' + text.replace('\n\n', ' ')
    text = text.replace('（','（質問者:')
    text = text.replace('）','？）')
    print(f'docx 全体の文字数: {len(text)}')

    # 先頭何文字まで読み込むか（API費用に関わる部分）
    max_text_length = 100000
    text = text[:max_text_length]
    print(f'モデルに学習させる文字数: {len(text)}')

    # txt 出力
    with open(f'data/data_txt/{filename}/{filename}.txt', mode='w') as f:
      f.write(text)

def set_deepl():
  global translator 
  translator = deepl.Translator(os.environ.get("DEEPL_KEY"))
  entries_ja_en = {"三ツ矢サイダー": "MITSUYA CIDER",
            "フリスク": "FRISK","パインアメ": "PINEAPPLE CANDY","龍角散": "RYUKAKUSAN","カルピス":"CALPICO",
            "果実のど飴": "FRUITS COUGH DROPS","透き通ったミントののど飴": "CLEAR MINT COUGH DROPS","濃ーいブルーベリー": "DARK BLUEBERRIES",
            "スーパーメントール": "SUPER MENTOL", "キシリクリスタル": "XYLYCRYSTAL", "和種ハッカ":"JAPANESE HAKKA", "和種ハッカのど飴":"JAPANESE HAKKA COUGH CROPS", "のど黒アメ":"NODOKUROAME",
            "カリンのど飴":"KARIN COUGH DROPS"
            } #まだ追加途中
  entries_en_ja = {"MITSUYA CIDER":"三ツ矢サイダー",
            "FRISK": "フリスク","PINEAPPLE CANDY": "パインアメ","RYUKAKUSAN":"龍角散","CALPICO": "カルピス",
            "FRUITS COUGH DROPS":"果実のど飴", "CLEAR MINT COUGH DROPS":"透き通ったミントののど飴", "DARK BLUEBERRIES":"濃ーいブルーベリー",
              "SUPER MENTOL":"スーパーメントール",  "XYLYCRYSTAL":"キシリクリスタル", "JAPANESE HAKKA":"和種ハッカ", "JAPANESE HAKKA COUGH CROPS":"和種ハッカのど飴", "NODOKUROAME":"のど黒アメ",
            "KARIN COUGH DROPS":"カリンのど飴"
            }
  glossary_ja_en = translator.create_glossary('My Dictionary JA', source_lang='JA', target_lang='EN', entries=entries_ja_en)
  glossary_en_ja = translator.create_glossary('My Dictionary EN', source_lang='EN', target_lang='JA', entries=entries_en_ja)
  global mydic_id_en_ja,mydic_id_ja_en
  mydic_id_ja_en = glossary_ja_en.glossary_id
  mydic_id_en_ja = glossary_en_ja.glossary_id

def translate_text():
  for i in range(num_docx):
    dir_path = f'data/data_txt/{i+1}'
    file_name = f'{i+1}.txt'
    file_path = os.path.join(dir_path, file_name)
    os.makedirs(f'data/data_translated_{i+1}',exist_ok = True)

    if not os.path.exists(f"data/data_translated_{i+1}/{i+1}_translated.txt"):
      with open(file_path) as f:
        lines = f.read()
        lines_translated = translator.translate_text(lines,source_lang="JA",target_lang="EN-US",glossary=mydic_id_ja_en)
      with open(f"data/data_translated_{i+1}/{i+1}_translated.txt", "w") as new_file:
        new_file.write(lines_translated.text)

def make_japanese_index():
  indexes = []
  # インデックスの作成
  for i in range(num_docx):
      dir_name = f'data/data_txt/{i+1}'
      documents = SimpleDirectoryReader(dir_name).load_data()
      index = GPTSimpleVectorIndex(
          documents=documents,
          prompt_helper=PromptHelper(
              max_input_size=4000,
              num_output=1000,
              max_chunk_overlap=0,
          )
      )
      indexes.append(index)
  return indexes

def make_english_index():
  indexes_translated = []

  # インデックスの作成
  for i in range(num_docx):
      dir_name = f'data/data_translated_{i+1}'
      documents = SimpleDirectoryReader(dir_name).load_data()
      index = GPTSimpleVectorIndex(
          documents=documents,
          prompt_helper=PromptHelper(
              max_input_size=4000,
              num_output=1000,
              max_chunk_overlap=0,
          )
      )
      indexes_translated.append(index)
  return indexes_translated

def create_index():
  if os.path.exists(f'data/data_index/index_en_1.json'):
    indexes_en = []
    for i in range(num_docx):
      index_en = GPTSimpleVectorIndex.load_from_disk(f'data/data_index/index_en_{i+1}.json')
      indexes_en.append(index_en)
  else:
    indexes_en = make_english_index()
    for i in range(num_docx):
      indexes_en[i].save_to_disk(f'data/data_index/index_en_{i+1}.json')

  
  if os.path.exists(f'data/data_index/index_ja_1.json'):
    indexes_ja = []
    for i in range(num_docx):
      index_ja = GPTSimpleVectorIndex.load_from_disk(f'data/data_index/index_ja_{i+1}.json')
      indexes_ja.append(index_ja)
  else:
    indexes_ja = make_japanese_index()
    for i in range(num_docx):
      indexes_ja[i].save_to_disk(f'data/data_index/index_ja_{i+1}.json')

  return [indexes_en,indexes_ja]  
  
