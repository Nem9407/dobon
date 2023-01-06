# ドボン

CPUとドボンで遊ぶことが出来ます


## 「ドボンの基本ルール」
手札のカードの数字の合計が場のカードの数字と同じとき、「ドボン」と宣言できます。  
ドボン出来た人の勝利となり、場のカードの数字の分だけその人の点数にプラスされます。  
ドボンされた人は場のカードの数字の分だけ点数がマイナスされます。  


ただし、次の状況のときは点数移動が2倍になります。
 * ドボン返し ... ドボンされたとき、自分の手札の合計も場のカードの数字と同じとき、ドボンを返すことが出来る。この場合はドボン返しした人の勝利となる。
 * 引きドボン ... カードを引いて手札の合計が場のカードの数字と同じになってドボンした場合。
 * 裏ドラ ... ドボンしたとき、ゲームの初めに1枚伏せてあるカードの数字が場のカードの数字と同じだった場合。
 * 山札が無くなった場合 ... 場に出ているカードをシャッフルして山札にします。これ以降、点数移動は2倍になります。


また、次の状況の時は点数移動が一定の点数で固定になります。
 * 「天保」(10点) ... 初めに3枚カードを配られた時点で手札のカードの数字の合計が場のカードの数字と同じとき。
 * 「手札が8枚以上」(15点) ... ターン終了時に手札が8枚以上の場合、負けとなります。


各プレイヤーは初め30点づつ持っており、どちらかのプレイヤーの持ち点が0以下になったとき、ゲーム終了となります。


## 「カードの出し方」
基本的に場のカードと同じマークか同じ数字のカードを出すことが出来ます。  
UNOのトランプ版のようなルールです。


## 「各種役札の説明」
### ・A(1),8,10
ドローカードです。場のカードと関係なく出すことが出来ます。  
カードを出した次の順番の人はカードを1枚とって手札に加えなければいけません。  
ただし、次の人もドローカードを持っていたら重ねて出すことが出来て、さらに次の人が2枚取らなければいけません。  
ドローカードを出せる限り、重ねて出すことが出来ます。

### ・J
万能カードです。場のカードがドローカード以外なら出すことが出来ます。  
このカードを出した人は次の人が出すカードのマークを指定することが出来ます。


## 「細かいルール」
順番に同じマークか同じ数字、役札を1枚出すことでゲームが進みます。  
カードを出して手札が無くなってしまった場合、カードを1枚引きます。  
手札の中に出せるカードがない場合、または出したくない場合は山札からカードを1枚引きます。  
それでもカードが出せない場合、または出したくない場合は「パス」と宣言することで次の人の手番になります。


## 「遊び方」
'dobon.py'を実行すれば遊べます。  
すでに山札がシャッフルされてプレイヤーとCPUに点数が30点づつ、カードが3枚づつ、場にカードが1枚配られている状態から始まります。  
初めの手札が全て11以上の時は手札を入れ替えることができます。


## 「未実装」
* 手札が8枚以上になったときの裏ゲーム
* ジョーカー
* CPUの思考能力
