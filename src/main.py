import question,make_index

#indexを作成して質問をする関数
#index作成してからはloadするのが良いので次回以降はその実装を行う
q = "質問者：あなたが飴を食べる頻度は？"
print("English Index")
question.question_to_translated(make_index.make_english_index,q)
print("---")
print("Japanes Index")
question.question_to_translated(make_index.make_japanese_index,q)
