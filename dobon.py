import random

#ジョーカー以外の54枚で山札を構築
card_mark = ['♠', '♣', '♥', '♦']
deck = [mark + str(num) for num in range(1,14) for mark in card_mark]

#変数の定義
game_count = 1
turn_count = 0
draw_count = 0
your_point = 30
cpu_point  = 30
game_rate = 1
blind_bonus = ''
draw_cards_list = [i+j for i in card_mark for j in ['1', '8', '10']]
eleven_choice = 'free'
win_player = ''
can_dobon = 'free'
drawed_dobon = False
tenho = False
penalty = False

#山札をシャッフル
random.shuffle(deck)

#指定した枚数だけカードを引く関数
#draw_deck:山札
#num:ドローする枚数
#dialogue:ドローしたことを出力するかどうか
def draw(draw_deck, num=0, dialogue=True):
    global game_rate
    global table

    #山札が無くなった場合
    if num > len(draw_deck):
        draw_deck.extend(table[:-1])
        random.shuffle(draw_deck)
        table = [table[-1]]
        game_rate *= 2
        print('山札が無くなりました、レートが二倍になります')
        print('---------------------') 

    #ドローしたことの出力
    if dialogue:
        print('カードを', num, '枚ドローしました')
        print('---------------------')  
    
    #num枚だけドローする
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
    global game_rate

    #カードを出す
    table.append(card_to_play)
    player.remove(card_to_play)
    print(card_to_play, 'を出しました')

    #ドボンできるかどうかを判定
    if turn == 0: can_dobon = 'cpu'
    else: can_dobon = 'you'

    #役札の場合
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

    #手札が無くなった場合
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
    global game_rate

    #プレイヤ―側
    if turn == 0:
        print('場のカード：', table[-1])
        print('あなたの手札：', player)
        print('カードを場に出すかパスしてください')
        print('カードを出す場合「マークと数字　例：♠1」、パスをする場合「pass」と入力してください')
        action = input()
        print('---------------------')
        while True:
            #カードを出す場合
            if action in you and (action[1:] == table[-1][1:] or action[0] == table[-1][0] or action[1:] in ['1', '8', '10', '11']): 
                to_play(player, action)
                break

            #パスをする場合
            elif action == 'pass': 
                print('パスしました')
                break
            
            #入力が正しくない場合
            else:
                print('入力が正しくありません。もう一度入力してください。')
                print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                action = input()

    else:
        card = player[-1]
        #カードを出す
        if (card in draw_cards_list) or card[1:] == '11' or (table[-1][1:] == '11' and card[0] == eleven_choice) or (card[0] == table[-1][0] or card[1:] == table[-1][1:]):
            to_play(computer, card)
            draw_check = False
        else: print('パスしました')

#ドボンできるかどうかを判定
def can_dobon_check(player):
    card_sum = 0
    for card in player: card_sum += int(card[1:])
    if table[-1][1:] == str(card_sum):
        #プレイヤー側
        if (can_dobon == 'you' or can_dobon == 'free') and turn == 0:
            print('あなたの手札：', you)
            print('ドボンできます！ドボンしますか？')
            print('「Yes」または「No」を入力してください ')
            you_ans = input()
            print('---------------------')

            if you_ans == 'Yes': return True
            else: return False

        #CPU側
        elif (can_dobon == 'cpu' or can_dobon == 'free') and turn == 1: return True
    else: return False


#ドボンの実装
while True:
    game_count = 1
    your_point = 30
    cpu_point  = 30
    while your_point > 0 and cpu_point > 0:
        #変数の初期化
        deck = [mark + str(num) for num in range(1,14) for mark in card_mark]
        random.shuffle(deck)
        turn_count = 0
        draw_count = 0
        game_rate = 1
        eleven_choice = 'free'
        win_player = ''
        can_dobon = 'free'
        drawed_dobon = False
        tenho = False

        #プレイヤー、コンピューター、場、裏ドラにカードを配る
        you = draw(deck, 3, False)
        computer = draw(deck, 3, False)
        table = draw(deck, 1, False)
        blind_bonus = draw(deck, 1, False)
        players = [you, computer]

        print('～～～', game_count, 'ゲーム目～～～')

        #1ゲーム分の処理
        while True:
            turn = turn_count % 2

            #手札の入れ替え判定
            if turn_count == 0:
                #プレイヤー側の処理
                change_check = True
                for card in you:
                    if not card[1:] in ['11', '12', '13']: change_check = False
                if change_check:
                    print(you)
                    print('手札が全て11以上です。手札を入れ替えることができます')
                    print('手札を入れ替えますか？入れ替える場合「Yes」、入れ替えない場合「No」と入力してください')
                    ans = input()
                    if ans == 'Yes':
                        deck.extend(you)
                        random.shuffle(deck)
                        you = draw(deck, 3, False)
                        print('手札を入れ替えました')
                        print('あなたの手札：', you)
                    print('---------------------')
                
                #CPU側の処理
                change_check = True
                for card in computer:
                    if not card[1:] in ['11', '12', '13']: change_check = False
                if change_check:
                    deck.extend(computer)
                    random.shuffle(deck)
                    computer = draw(deck, 3, False)
                    print('CPUが手札を入れ替えました')
                    print('---------------------')                    

            #ドボンできるかどうかを判断
            if turn == 0 and can_dobon_check(you):
                win_player = 'you'
                if turn_count == 0: tenho = True
                break
            elif (turn == 1 or turn_count == 0) and can_dobon_check(computer):
                win_player = 'cpu'
                if turn_count == 0: tenho = True
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

                    while True:
                        #ドローする場合
                        if action == 'draw':
                            draw_cards = draw(deck, draw_count)
                            you.extend(draw_cards)
                            draw_count = 0

                            #ドボンできるかどうかを判定
                            if can_dobon_check(you):
                                win_player = 'you'
                                drawed_dobon = True
                                break

                            print('場のカード：', table[-1])
                            print('あなたの手札：', you)
                            print('カードを出すか山札からもう1枚カードを引いてください')
                            print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                            action = input()
                            print('---------------------')

                            while True:
                                #さらにドローする場合
                                if action == 'draw':
                                    you.extend(draw(deck, 1))

                                    #ドボンできるかどうかを判定
                                    if can_dobon_check(you):
                                        win_player = 'you'
                                        drawed_dobon = True  
                                    else: pass_or_play(you, deck)
                                    break

                                #カードを出す場合
                                elif action in you and (action[1:] == table[-1][1:] or action[0] == table[-1][0] or action[1:] in ['1', '8', '10', '11']): 
                                    to_play(you, action)
                                    break
                                
                                #入力が正しくない場合
                                else:
                                    print('入力が正しくありません。もう一度入力してください。')
                                    print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                                    action = input()
                            break

                        #カードを出す場合
                        elif action in you and action in draw_cards_list:
                            to_play(you, action)
                            break

                        #入力が正しくない場合
                        else:
                            print('入力が正しくありません。もう一度入力してください。')
                            print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                            action = input()
                

                #場のカードが11
                elif table[-1][1:] == '11':
                    #1ターン目の場合
                    if eleven_choice == 'free':
                        print('好きなカードを出すか、カードを1枚引いてください')
                        print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                        action = input()
                        print('---------------------')

                        while True:
                            #ドローする場合
                            if action == 'draw': 
                                you.extend(draw(deck, 1))

                                #ドボンできるかどうかを判定
                                if can_dobon_check(you):
                                    win_player = 'you'
                                    drawed_dobon = True   
                                else: pass_or_play(you, deck)
                                break

                            #カードを出す場合
                            elif action in you: 
                                to_play(you, action)
                                break
                            
                            #入力が正しくない場合
                            else:
                                print('入力が正しくありません。もう一度入力してください。')
                                print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                                action = input()

                        
                    #2ターン目以降の場合
                    else:
                        print('場にあるカードは11です。マークが', eleven_choice, 'のカードを出すか、カードを1枚引いてください')
                        print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                        action = input()
                        print('---------------------')
                        
                        while True:
                            #ドローする場合
                            if action == 'draw': 
                                you.extend(draw(deck, 1))

                                #ドボンできるかどうかを判定
                                if can_dobon_check(you):
                                    win_player = 'you'
                                    drawed_dobon = True   
                                else: pass_or_play(you, deck)
                                break

                            #カードを出す場合
                            elif action in you and (action[0] == eleven_choice or action[1:] in ['1', '8', '10', '11']): 
                                to_play(you, action)
                                break

                            #入力が正しくない場合
                            else:
                                print('入力が正しくありません。もう一度入力してください。')
                                print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                                action = input()
                

                #場のカードがそれ以外
                else:
                    print('カードを出すか、カードを1枚引いてください')
                    print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                    action = input()
                    print('---------------------')

                    while True:
                        #ドローする場合
                        if action == 'draw': 
                            you.extend(draw(deck, 1))

                            #ドボンできるかどうかを判定
                            if can_dobon_check(you):
                                win_player = 'you'
                                drawed_dobon = True
                            else: pass_or_play(you, deck)
                            break

                        #カードを出す場合
                        elif action in you and (action[1:] == table[-1][1:] or action[0] == table[-1][0] or action[1:] in ['1', '8', '10', '11']):
                            to_play(you, action)
                            break
                        
                        #入力が正しくない場合
                        else:
                            print('入力が正しくありません。もう一度入力してください。')
                            print('カードを出す場合「マークと数字　例：♠1」、ドローする場合「draw」と入力してください')
                            action = input()

                #ドボンできる場合、ゲームを終了
                if win_player == 'you': break

                #手札が8枚以上の場合、ゲームを終了
                if len(you) >= 8:
                    penalty = True
                    win_player = 'cpu'
                    break       



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
                        draw_count = 0

                        #ドボンできるかどうかを判定
                        if can_dobon_check(computer):
                            win_player = 'cpu'
                            drawed_dobon = True
                            break

                        for card in computer:
                            if card in draw_cards_list or card[1:] == '11' or card[0] == table[-1][0]:
                                to_play(computer, card)
                                draw_check = False
                                break

                        if draw_check:
                            computer.extend(draw(deck, 1))

                            #ドボンできるかどうかを判定
                            if can_dobon_check(computer):
                                win_player = 'cpu'
                                drawed_dobon = True
                                break   
                            else: pass_or_play(computer, deck)

                
                #場のカードが11
                elif table[-1][1:] == '11':
                    for card in computer:
                        #カードを出す
                        if card in draw_cards_list or card[1:] == '11' or card[0] == eleven_choice:
                            to_play(computer, card)
                            draw_check = False
                            break
                        
                    #カードを出していない場合にドローする
                    if draw_check: 
                        computer.extend(draw(deck, 1))

                        #ドボンできるかどうかを判定
                        if can_dobon_check(computer):
                            win_player = 'cpu'
                            drawed_dobon = True
                            break   
                        else: pass_or_play(computer, deck)
                
                #場のカードがそれ以外
                else:
                    for card in computer:
                        #出せたらカードを出す
                        if card[0] == table[-1][0] or card[1:] == table[-1][1:] or (card in draw_cards_list) or (card[1:] == '11'):
                            to_play(computer, card)
                            draw_check = False
                            break
                    
                    #カードを出していない場合にドローする
                    if draw_check: 
                        computer.extend(draw(deck, 1))

                        #ドボンできるかどうかを判定
                        if can_dobon_check(computer):
                            win_player = 'cpu'
                            drawed_dobon = True
                            break   
                        else: pass_or_play(computer, deck)
                
                #手札が8枚以上の場合、ゲームを終了
                if len(computer) >= 8:
                    penalty = True
                    win_player = 'you'
                    break  
            
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

        #手札が8枚以上の場合
        if penalty:
            if win_player == 'you':
                print('CPUの手札が8枚以上になりました、あなたの勝ちです！')
                print('点数は15点です！')
                your_point += 15
                cpu_point -= 15
            elif win_player == 'cpu':
                print('あなたの手札が8枚以上になりました、CPUの勝ちです！')
                print('点数は15点です！')
                your_point -= 15
                cpu_point += 15

        #プレイヤーがドボンした場合
        elif win_player == 'you':
            #天保の場合
            if tenho == True:
                print('あなたの勝ちです！')
                print('天保なので、点数は10点です！')
                your_point += 10
                cpu_point -= 10

            #ドボン返しされない場合
            elif not hand_match: 
                print('あなたの勝ちです！')

                #引きドボンの確認
                if drawed_dobon:
                    print('引きドボンです！点数が2倍になります！')
                    game_rate *= 2

                #裏ドラの確認
                if blind_bonus[1:] == table[-1][1:]:
                    print('裏ドラが乗りました！点数が2倍になります！')
                    game_rate *= 2

                #点数の出力
                print('点数は', hand[0]*game_rate, '点です！')
                your_point += hand[0]*game_rate
                cpu_point -= hand[0]*game_rate

            #ドボン返しされた場合
            else: 
                print('CPUにドボン返しされました、CPUの勝ちです！点数は2倍になります！')
                game_rate *= 2

                #引きドボンの確認
                if drawed_dobon:
                    print('引きドボンです！点数が2倍になります！')
                    game_rate *= 2

                #裏ドラの確認
                if blind_bonus[1:] == table[-1][1:]:
                    print('裏ドラが乗りました！点数がさらに2倍になります！')
                    game_rate *= 2

                #点数の出力
                print('点数は', hand[1]*game_rate, '点です！')
                your_point -= hand[1]*game_rate
                cpu_point += hand[1]*game_rate

        #CPUがドボンした場合
        elif win_player == 'cpu':
            #天保の場合
            if tenho == True:
                print('CPUの勝ちです！')
                print('天保なので、点数は10点です！')
                your_point -= 10
                cpu_point += 10

            #ドボン返しできない場合 
            elif not hand_match: 
                print('CPUがドボンしました、CPUの勝ちです！')

                #引きドボンの確認
                if drawed_dobon:
                    print('引きドボンです！点数が2倍になります！')
                    game_rate *= 2

                #裏ドラの確認
                if blind_bonus[1:] == table[-1][1:]:
                    print('裏ドラが乗りました！点数が2倍になります！')
                    game_rate *= 2

                #点数の出力
                print('点数は', hand[1]*game_rate, '点です！')
                your_point -= hand[1]*game_rate
                cpu_point += hand[1]*game_rate

            #ドボン返しできる場合
            else: 
                print('CPUにドボンされましたがドボン返ししました、あなたの勝ちです！点数は2倍になります！')
                game_rate *= 2

                #引きドボンの確認
                if drawed_dobon:
                    print('引きドボンです！点数が2倍になります！')
                    game_rate *= 2

                #裏ドラの確認
                if blind_bonus[1:] == table[-1][1:]:
                    print('裏ドラが乗りました！点数がさらに2倍になります！')
                    game_rate *= 2
                    
                #点数の出力
                print('点数は', hand[0]*game_rate, '点です！')
                your_point += hand[0]*game_rate
                cpu_point -= hand[0]*game_rate


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
    print('---------------------')

    print('Enterキーを押したら終了します')
    print('もう一度遊びたい場合は何か文字を入力して下さい')
    key = input()
    if key == '': break