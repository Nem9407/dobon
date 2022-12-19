import random

#ジョーカー以外の54枚で山札を構築
card_mark = ['♠', '♣', '♥', '♦']
deck = [mark + str(num) for num in range(1,14) for mark in card_mark]

#変数の定義
game_count = 1
turn_count = 0
draw_count = 0
dobon_num = 0
your_point = 30
cpu_point  = 30
game_rate = 1
blind_bonus = ''
draw_cards_list = [i+j for i in card_mark for j in ['1', '8', '10']]
eleven_choice = 'free'
win_player = ''
can_dobon = 'free'

#山札をシャッフル
random.shuffle(deck)

#指定した枚数だけカードを引く関数
#draw_deck:山札
#num:ドローする枚数
def draw(draw_deck, num=0):
    cards = []
    for i in range(num):
        draw_card = draw_deck[0]
        cards.append(draw_card)
        draw_deck.remove(draw_card)
    return cards

#player が card_to_play を場に出す関数
#player:カードを出す人
#card_to_play:場に出すカード
def to_play(player, card_to_play):
    global draw_count
    global can_dobon
    global eleven_choice
    global table

    table.append(card_to_play)
    player.remove(card_to_play)
    print(card_to_play, 'を出しました')
    if turn == 0: can_dobon = 'cpu'
    else: can_dobon = 'you'

    if card_to_play[1:] == '11':
        if turn == 0:
            print('マークを指定してください　例：♠')
            eleven_choice = input()
            print('---------------------')
            print(eleven_choice, 'を指定しました')
        else: 
            eleven_choice = random.choice(['♠', '♣', '♥', '♦'])
            print('CPUは', eleven_choice, 'を指定しました')
    elif card_to_play[1:] in ['1', '8', '10']: 
        draw_count += 1

    if len(player) == 0: 
        draw_cards = draw(deck, 1)
        player.extend(draw_cards)
        print('手札が0枚になったので1枚ドローしました')

#ドローをしてパスまたはカードを出す関数
#player:パスまたはドローする人
#draw_deck:山札
def pass_or_play(player, draw_deck):
    global draw_check
    global draw_count
    global can_dobon
    global eleven_choice
    global table

    player.extend(draw(draw_deck, 1))
    print('カードを1枚ドローしました')
    print('---------------------')

    if turn == 0:
        print('場のカード：', table[-1])
        print('あなたの手札：', player)
        print('CPUの手札：', computer)
        print('カードを場に出すかパスしてください')
        print('カードを出す場合「マークと数字　例：♠1」、パスをする場合「pass」と入力してください')
        action = input()
        print('---------------------')
        if action in player: to_play(player, action)
        elif action == 'pass': print('パスしました')
    else:
        card = player[-1]
        #カードを出す
        if (card in draw_cards_list) or card[1:] == '11' or (table[-1][1:] == '11' and card[0] == eleven_choice) or (card[0] == table[-1][0] or card[1:] == table[-1][1:]):
            to_play(computer, card)
            draw_check = False
        else: print('パスしました')



#ドボンの実装
while your_point > 0 and cpu_point > 0:
    #変数の初期化
    deck = [mark + str(num) for num in range(1,14) for mark in card_mark]
    random.shuffle(deck)
    turn_count = 0
    draw_count = 0
    dobon_num = 0
    game_rate = 1
    blind_bonus = ''
    eleven_choice = 'free'
    win_player = ''
    can_dobon = 'free'

    #プレイヤー、コンピューター、場、裏ドラにカードを配る
    you = draw(deck, 3)
    computer = draw(deck, 3)
    table = draw(deck, 1)
    blind_bonus = draw(deck, 1)
    players = [you, computer]

    print('～～～', game_count, 'ゲーム目～～～')

    #1ゲーム分の処理
    while True:
        turn = turn_count % 2

        #ドボンできるかどうかを判断
        card_sum = 0
        for card in players[turn]: card_sum += int(card[1:])
        if table[-1][1:] == str(card_sum):

            #プレイヤー側
            if turn == 0:
                print('ドボンできます！ドボンしますか？')
                print('「Yes」または「No」を入力してください ')
                you_ans = input()
                print('---------------------')
                if you_ans == 'Yes':
                    win_player = 'you'
                    dobon_num = card_sum
                    break
            
            #CPU側
            else:
                win_player = 'CPU'
                dobon_num = card_sum
                break
        
        #プレイヤー側の処理
        if turn == 0:

            #現在の状況を出力
            print('-----あなたのターン-----')
            print('山札の残り枚数：', len(deck), '枚')
            print('場のカード：', table[-1])
            print('あなたの手札：', you)
            print('CPUの手札の枚数：', len(computer), '枚')
            print('---------------------')


            #状況ごとに行動を選択

            #場のカードがドローカード
            if table[-1] in draw_cards_list and turn_count != 0 and draw_count != 0:
                print('場にあるカードはドローカードです。ドローカードを出すか山札から', draw_count, '枚引いてください')
                print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                action = input()
                print('---------------------')

                #ドローする場合
                if action == 'draw':
                    draw_cards = draw(deck, draw_count)
                    you.extend(draw_cards)
                    print('カードを', draw_count, '枚ドローしました')
                    draw_count = 0

                    print('場のカード：', table[-1])
                    print('あなたの手札：', you)
                    print('カードを出すか山札からもう1枚カードを引いてください')
                    print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                    action = input()
                    print('---------------------')
                    if action == 'draw': pass_or_play(you, deck)
                    else: 
                        #ここに出せるカードかを判定する処理を記述する
                        to_play(you, action)
                        can_dobon = 'cpu'


                #カードを出す場合
                else:
                    #ここに1,8,10だけを通す処理を記述する
                    to_play(you, action)
                    can_dobon = 'cpu'
            

            #場のカードが11
            elif table[-1][1:] == '11':
                if eleven_choice == 'free':
                    print('好きなカードを出すか、カードを1枚引いてください')
                    print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                    action = input()
                    print('---------------------')

                    #ドローする場合
                    if action == 'draw': pass_or_play(you, deck)

                    #カードを出す場合
                    else: to_play(you, action)
                else:
                    print('場にあるカードは11です。マークが', eleven_choice, 'のカードを出すか、カードを1枚引いてください')
                    print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                    action = input()
                    print('---------------------')
                    
                    #ドローする場合
                    if action == 'draw': pass_or_play(you, deck)

                    #カードを出す場合
                    else: 
                        #ここに指定のマークだけを通す処理を記述する
                        to_play(you, action)
            

            #場のカードがそれ以外
            else:
                print('カードを出すか、カードを1枚引いてください')
                print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                action = input()
                print('---------------------')

                #ドローする場合
                if action == 'draw': pass_or_play(you, deck)

                #カードを出す場合
                else:
                    #ここにカードを出せるかどうかの判定を記述
                    to_play(you, action)


        #CPU側の処理
        else:
            print('-----CPUのターン-----')
            
            #状況ごとに行動を選択
            draw_check = True

            #場のカードがドローカード
            if table[-1] in draw_cards_list and draw_count != 0:

                #カードを出す場合
                for card in computer:
                    if card in draw_cards_list:
                        to_play(computer, card)
                        draw_check = False
                        break

                #ドローする場合
                if draw_check:
                    draw_cards = draw(deck, draw_count)
                    computer.extend(draw_cards)
                    print('カードを', draw_count, '枚ドローしました')
                    draw_count = 0

                    for card in computer:
                        if card in draw_cards_list or card[1:] == '11' or card[0] == table[-1][0]:
                            to_play(computer, card)
                            draw_check = False
                            break
                    if draw_check: pass_or_play(computer, deck)

            
            #場のカードが11
            elif table[-1][1:] == '11':
                for card in computer:
                    #カードを出す
                    if card in draw_cards_list or card[1:] == '11' or card[0] == eleven_choice:
                        to_play(computer, card)
                        draw_check = False
                        break
                    
                #カードを出していない場合にドローする
                if draw_check: pass_or_play(computer, deck)
            
            #場のカードがそれ以外
            else:
                for card in computer:
                    #出せたらカードを出す
                    if card[0] == table[-1][0] or card[1:] == table[-1][1:] or (card in draw_cards_list) or (card[1:] == '11'):
                        to_play(computer, card)
                        draw_check = False
                        break
                
                #カードを出していない場合にドローする
                if draw_check: pass_or_play(computer, deck)
        
        #ターン数を増やす
        turn_count += 1


    #手札が一致してるかどうかの判定
    hand_match = False
    hand = []
    for player in players:
        card_sum = 0
        for card in player: card_sum += int(card[1:])
        hand.append(card_sum)
    if hand[0] == hand[1]: hand_match = True


    #結果の出力

    #プレイヤーがドボンした場合
    if win_player == 'you':
        #ドボン返しされない場合
        if not hand_match: 
            print('あなたの勝ちです！')

            #裏ドラの確認
            if blind_bonus[1:] == table[-1][1:]:
                print('裏ドラが乗りました！点数が2倍になります！')
                game_rate *= 2

            print('点数は', hand[0]*game_rate, '点です！')
            your_point += hand[0]*game_rate
            cpu_point -= hand[0]*game_rate

        #ドボン返しされた場合
        else: 
            print('CPUにドボン返しされました、CPUの勝ちです！点数は2倍になります！')
            game_rate *= 2

            #裏ドラの確認
            if blind_bonus[1:] == table[-1][1:]:
                print('裏ドラが乗りました！点数がさらに2倍になります！')
                game_rate *= 2

            print('点数は', hand[1]*game_rate, '点です！')
            your_point -= hand[1]*game_rate
            cpu_point += hand[1]*game_rate

    #CPUがドボンした場合
    elif win_player == 'CPU':
        #ドボン返しできない場合 
        if not hand_match: 
            print('CPUがドボンしました、CPUの勝ちです！')

            #裏ドラの確認
            if blind_bonus[1:] == table[-1][1:]:
                print('裏ドラが乗りました！点数が2倍になります！')
                game_rate *= 2

            print('点数は', hand[1]*game_rate, '点です！')
            your_point -= hand[1]*game_rate
            cpu_point += hand[1]*game_rate

        #ドボン返しできる場合
        else: 
            print('CPUにドボンされましたがドボン返ししました、あなたの勝ちです！点数は2倍になります！')
            game_rate *= 2

            #裏ドラの確認
            if blind_bonus[1:] == table[-1][1:]:
                print('裏ドラが乗りました！点数がさらに2倍になります！')
                game_rate *= 2
                
            print('点数は', hand[0]*game_rate, '点です！')
            your_point += hand[0]*game_rate
            cpu_point -= hand[0]*game_rate
    else: print('山札が無くなってしまいました')

    #1ゲームが終了
    game_count += 1

    #どちらかの持ち点が0以下かどうかを判定
    if your_point <= 0 or cpu_point <= 0: break
    else:
        #持ち点の出力
        print('---------------------')
        print('あなたの持ち点：', your_point, '点')
        print('CPUの持ち点：', cpu_point, '点\n')


#最終結果の出力
print('\n-----最終結果-----')
if cpu_point <= 0: print('CPUの持ち点が0点以下になりました、あなたの勝ちです！')
else: print('あなたの持ち点が0点以下になりました、CPUの勝ちです！')