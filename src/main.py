import question,make_index

#環境変数の設定、indexを作成するための翻訳txtファイルの用意、deeplのglossaryの設定
make_index.set_env()
make_index.set_deepl()
make_index.translate_text() #元々ファイルがあれば作成しない

#indexがjsonで保存されていればそれをloadする、indexが保存されていなければ作成してsaveする
[indexes_en,indexes_ja] = make_index.create_index()

#作成したindexに対して質問する
print("Indexに対して質問したいことを「質問者:---?」の形で書いてください")
q = input()
#翻訳されたIndexに対して質問
print("Question to Translated Index")
question.question_to_translated(indexes_en,q)
print("---")
#翻訳していないIndexに対して質問
print("Question to Japanese Index")
question.question_to_japanese(indexes_ja,q)
