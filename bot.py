from typing import Final, List, Dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater, CallbackQueryHandler, CallbackContext, ConversationHandler
import asyncio
import random

TOKEN: Final = '7493150219:AAFxx-Ryk-Cz_cI4PoWXgim91ioFkI2VN98'
BOT_USERNAME: Final = '@sheepsleepbot'
金句 = ['你今日抽到１隻羊！唔好灰心！' , '你今日抽到2隻羊！' , '你今日抽到3隻羊！' , '你今日抽到4隻羊！' , '你今日抽到5隻羊！', '你今日抽到6隻羊！', '你今日抽到7隻羊！', '你今日抽到8隻羊！', '你今日抽到9隻羊呀！犀利！', '你今日抽到10隻羊呀！今日係你既Lucky Day！']
TEAM = {"A": "村民陣營",
        "B": "狼人陣營"
}


#Callbacks
async def callback(update: Update, context: CallbackContext):
    group_id = update.callback_query.message.chat.id
    user = update.callback_query.from_user
    query_data = update.callback_query.data
    print(user.first_name)
    if 'command' in query_data:
        if group_id not in data:
            return
    if query_data == '/join_command':
        if user in data[group_id]['players']:
            return
        await join(update, context, group_id, user)
    elif query_data == '/flee_command':
        await flee(update, context, group_id, user)
    elif query_data == '/start_command':
        await start(update, context, group_id, user)
    elif 'rs_' in query_data:
        group_id = data[user.id]['group_id']
        if '村長' not in data[group_id]:
            return
        if user != data[group_id]['村長']:
            return
        if 'spell' in data[group_id]:
            return
        print('rs')
        spell = query_data.replace('rs_','')
        print('spell')
        data[group_id]['spell'] = spell
        await context.bot.send_message(
            chat_id=data[group_id]['村長'].id,
            text=f"你的選擇是 {spell}。")
        print('abc', context)
        await abc(update, context, group_id, user)

#Commands

async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.message.chat.id
    chat_id = update.message.chat.id
    user = update.message.from_user
    bot = context.bot

    if chat_id not in [-1001216470197, -1001177780147, -1001598549945]:
        bot.send_message(chat_id, "若要玩驚谷羊人殺請申請加入專屬遊戲群組(只限幼女會員) tg @lmdeedee")
        bot.send_message(266799002,
                         user.id + ": " + user.first_name + "\n Group: " + chat_id + ": " + update.message.chat.title)
        print(user.id + ": " + user.first_name + "\n Group: " + chat_id + ": " + update.message.chat.title)

    if group_id > 0:
        await update.message.reply_text("呢個command只可以用喺group到用㗎。")
        return
    # Store the game data in the context, including the group ID, players, etc.
    if group_id not in data:
        data[group_id] = {
            "players": [],
            "started": False
        }
    # Check if the game is already running
    if data[group_id]['started']:
        await update.message.reply_text('遊戲已經開始咗啦，下次請早！')
        return
    # Get the bot instance from the context
    bot = context.bot
    # join/flee/start buttons
    if 'newmsgid' in data[group_id]:
        await context.bot.deleteMessage(group_id, data[group_id]['newmsgid'])
    players_name = [p.first_name for p in data[group_id]['players']]
    text = (f"歡迎加入驚谷狼人真言!遊戲人數4~11!\n"
            f"{','.join(players_name)}")
    msg = await bot.send_message(
        chat_id=group_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("/join", callback_data="/join_command",),
                InlineKeyboardButton("/flee", callback_data="/flee_command"),
                InlineKeyboardButton("/start", callback_data="/start_command"),
            ]]
        )
    )
    data[group_id]['newmsgid'] = msg.message_id
    # Print the group ID and the current player list
    print(f"Group ID: {group_id}")
    print(f"Players:{data[group_id]}['players']")


async def join_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.message.chat.id
    user = update.message.from_user
    # Check if command is used in a group
    if group_id > 0:
        await update.message.reply_text("呢個command只可以用喺group到用㗎。")
        return
    # Check if a game exists in the group
    if group_id not in data:
        await update.message.reply_text("呢個group重未有game開始，快啲開返個啦！")
        return
    # Check if the game is already running
    if data[group_id]['started']:
        await update.message.reply_text('遊戲已經開始咗啦，下次請早！')
        return
    # Check if the user is already in the game
    if user in data[group_id]['players']:
        await update.message.reply_text('你已經喺遊戲入面啦！')
        return
    # Add the user to the game
    await update.message.reply_text(f'{group_id}左腳kick右腳，右腳又kick左腳，咁都趕得切尾班車入埸！')
    print(f'User ({update.message.from_user.first_name}) joined the game in group {group_id}')
    await join(update, context, group_id, user)


async def join(update, context, group_id, user):
    try:
        await context.bot.sendMessage(chat_id=user.id,
            text="你已經加入" + update.callback_query.message.chat.title + "的遊戲中!")
    except:
        await context.bot.sendMessage(chat_id=group_id, text=user.first_name + " 請先啟動我!",
            reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("按我啟動", url="t.me/sheepsleepbot")]]))
        return
    data[group_id]['players'].append(user)
    data[user.id] = {'group_id':group_id}
    name = user.first_name
    players_name = [p.first_name for p in data[group_id]['players']]
    text = (f"歡迎加入驚谷狼人真言!遊戲人數4~11!\n"
            f"{','.join(players_name)}")
    if 'newmsgid' in data[group_id]:
        await context.bot.deleteMessage(group_id, data[group_id]['newmsgid'])
    msg = await context.bot.send_message(
        chat_id=group_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("/join", callback_data="/join_command", ),
                InlineKeyboardButton("/flee", callback_data="/flee_command"),
                InlineKeyboardButton("/start", callback_data="/start_command"),
            ]]
        )
    )
    data[group_id]['newmsgid'] = msg.message_id

async def flee_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.message.chat.id
    user = update.message.from_user
    await flee(update, context, group_id, user)

async def flee(update, context, group_id, user):
    # Remove user from players
    data[group_id]["players"].remove(user)
    # Send confirmation message
    await context.bot.send_message(
        chat_id=group_id,
        text=f"{user.first_name} 離開遊戲!")  # Done
    name = user.first_name
    players_name = [p.first_name for p in data[group_id]['players']]
    text = (f"歡迎加入驚谷狼人真言!遊戲人數4~11!\n"
            f"{','.join(players_name)}")
    if 'newmsgid' in data[group_id]:
        await context.bot.deleteMessage(group_id, data[group_id]['newmsgid'])
    msg = await context.bot.send_message(
        chat_id=group_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("/join", callback_data="/join_command", ),
                InlineKeyboardButton("/flee", callback_data="/flee_command"),
                InlineKeyboardButton("/start", callback_data="/start_command"),
            ]]
        )
    )
    data[group_id]['newmsgid'] = msg.message_id


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.message.chat.id
    user = update.message.from_user
    await start(update, context, group_id, user)

async def start(update, context, group_id, user):
    print(data[group_id])
    if data[group_id]['started']:
        return
    # Check if enough players
    if len(data[group_id]['players']) < 4 or len(data[group_id]['players']) > 11:
        await context.bot.send_message(
            chat_id=group_id,
            text="遊戲人數不足或過多!請至少4人，最多11人!"
        )
        return

    data[group_id]['started'] = True
    data[group_id]['yn'] = 0
    data[group_id]['?'] = 0
    await context.bot.deleteMessage(group_id, data[group_id]['newmsgid'])

    players = data[group_id]['players'].copy()
    data[group_id]['村長'] = random.choice(players)#[p for p in data[group_id]['players'] if p.id == 544681898][0]random.choice(players)
    data[group_id]['先知'] = random.choice(players)
    players.remove(data[group_id]['先知'])
    if len(data[group_id]['players']) > 7:
        data[group_id]['狼人'] = random.sample(players, 2)
    else:
        data[group_id]['狼人'] = random.sample(players, 1)
    for p in data[group_id]['狼人']:
        players.remove(p)
    data[group_id]['村民'] = [p for p in players.copy() if p != data[group_id]['村長']]

    print(data[group_id])
    # PM通知玩家角色
    await context.bot.send_message(
        chat_id=data[group_id]['村長'].id,
        text="你的角色是 {村長}。"
    )
    await context.bot.send_message(
        chat_id=data[group_id]['先知'].id,
        text="你的角色是 {先知}。"
    )
    for p in data[group_id]['狼人']:
        await context.bot.send_message(
            chat_id=p.id,
            text="你的角色是 {狼人}。"
        )
    for p in data[group_id]['村民']:
        await context.bot.send_message(
            chat_id=p.id,
            text="你的角色是 {廢村}。"
        )
#---------------------------------------------------------------------------------------------------OK線
        # 抽選咒語
    spell = ['曼聯', '陳柏宇', '郭晉安', '周柏豪', 'NewJeans', '張國榮', '張學友', '張敬軒', '方大同', '李克勤',
                  '林子祥', 'Faker', '小海白', '小薯茄', '試當真', '郭富城', '鄭中基', '陳偉霆', '陳奕迅', '黎明',
                  '13B', '奧雲', '牛哥','炎明熹', '羊妹', 'IVYSO', '楊千嬅', '泳兒', '謝安琪', '關心妍 ', 'COLLAR',
                  'LollyTalk', 'Twins', '吳千語','黃心穎','食神', '英皇娛樂', '娛樂圈', '畢打自己人', '愛回家', '做完愛回家', '蘭陵王 ', '方東昇',
                  '童夢奇緣', '這個殺手不太冷', '星夢傳奇', '100毛', '美少女戰士', '忠犬小八', '鹿鼎記', '午夜凶鈴',
                  '女王的教室', '龍咁威', '天與地', '一公升眼淚', '西遊記', '阿甘正傳', '阿信的故事', '少林足球',
                  '老夫子','蘭桂坊', '大嶼山', '超大型巨人', '親子王國', '哈爾濱', '油麻地', '金枝慾孽', '貓哭老鼠', '三哥',
                  '譚仔', '白兔糖', '首爾', '龜兔賽跑', '怕醜草', '東涌', '涼茶', '墨魚丸', '秘書', '果仁', '火車',
                  '古天樂', '約旦', '黑馬','田泰安', '巴度', '潘頓', '莫雷拉', '勁歌金曲', '四洲紫菜', '目黑 ', '李白',
                  '葡萄酒', '跳傘', '絲打''巴打','零食物語', '凍朱古力', '凍檸蜜', '下午茶', '四季豆', '美心西餅', '公仔麵', '凍檸茶', '月餅',
                  '奶皇包', '花之戀', '大家樂', '蘋果日報', '風雲', '一見鍾情', '兒孫滿堂', '難兄難弟', '百發百中',
                  '無聲彷有聲', '薔薇之戀', '車路士', '紅樓夢', '蛇鼠一窩','跑馬地', '上環', '金鐘', '東方日報', '十年',
                  '富士山下', '獅子山下', '明年今日', '失憶蝴蝶', '先哭為敬', '安妮亞', '兩餸飯','夕陽無限好', '大嶼山', '上海', '親子王國', '北角', '張國榮', '麥芽糖','安眠藥',
                  '番薯糖水', '乳酪', '葉劉淑儀', '土耳其', '瘦身男女', '千尋', '炎柱', '襲警', '屎撈人', '閃電傳真機','母雞',
                  '天鵝','鱷魚','西瓜','田螺','醬油','糯米飯','隱形眼鏡','燈籠','扣子','鋤頭','害羞','下棋','唱歌','射擊','垂頭喪','憤怒','周杰倫',
                  '饅頭','變形金剛','楊貴妃','南瓜','茄子','花生油','披薩','口紅','火鍋','股票','圓規','鐵錘','喝水','暗戀','噴香水','打電話','面條','咳嗽','感冒','火山爆發',
                  '一刀兩斷','月亮 ','鴨子','大肥豬','哈密瓜','宵夜','公仔面','剪刀','凳子','彩票','鏟子','指甲油','毛筆','美女','吃醋','跳舞','牙疼','假貨',
                  '和尚','太陽 ','水牛','狐貍','榴蓮','巧克力','香腸','雨傘','電筒','車票','橡皮擦','鉗子','鞋帶','唱歌','鬚','謝謝','發冷','冷笑','金雞獨立','尼姑',
                  '星星','大象','老鷹','鸚鵡','蓮蓬','柚子','雪糕','冰淇淋','餅乾','雨衣','溫度計','白內障','鐮刀','酸','放屁','剃頭','肌肉','血壓','肚痛','武則天',
                  '婦女節','山羊','鯨魚','河馬','大蒜','橙子','鵪鶉蛋','菜刀','聽診器','剃須刀','白糖','粉筆','辣','開車','洗手','對不起','喝酒','頭痛','打噴嚏','三長二短','生姜','葡萄',
                  '蛋糕','滅火器','手錶','沐浴露','黑板刷','放風箏','搶劫','消毒','抱歉','網購','嚇一跳','寒戰','貂蟬','天安門','黃絲','藍絲','杜文澤','兵馬俑','兒童節','造紙','口罩',
                  '汽油彈','猴子','驢','別怪他','蜈蚣','蘋果','芝麻','貓女郎','蝙蝠俠','閃電俠','超人','雷神','美國隊長','鋼鐵人','蒼井空','餛飩','香皂','寶馬','烈火戰車','櫻花樹下',
                  '羅生門','項鏈','假牙','老公','睡覺','發夢','同意','跳繩','長城','武松','摩天輪','青蛙','螞蟻','蝗蟲','水貨客','雪梨','甘蔗','香港','領事館','金屬','玫瑰花','斑馬',
                  '麻雀','滑鼠','鍵盤','望遠鏡','計數機','高踭鞋','茉莉花','櫻花','向日葵','菊花','薰衣草','鄧紫棋','武肺','解放軍','垃圾桶','肛交 ','狗仔式','觀音坐蓮','鄧麗欣','男排女將',
                  '方力申','大衛','自由神像','索爾','衛生巾','安全套','背囊','爆炸糖','香煙','農場','小說','黑死病','燕子','拉筋','莎士比亞','關羽','李斯','新垣結衣','佩佩豬','噴火龍','愛回家',
                  '流浪漢','烏龍茶','太極','火星','蝙蝠','移民','微波爐','信用卡','瘟神','髮型師','核爆','一石二鳥','感動','歪理','鐮刀','箭頭','解剖','愚公移山','核心','進化論','基因','冥想',
                  '雪崩','刺身','黃昏','塔羅牌','見字飲水','遊戲王','八卦','天竺鼠車車','十兄弟','成績表','資本主義','復古','大地色','倒立','二頭肌','蝦片','心太軟','火鍋','情人節','大減價','遲到',
                  '影子','歌詞','殖民地','壁畫','跟蹤狂','行程','民宿','狗屋','鐵達尼號','奧斯卡','人工智能','畫家帽','清酒','鸚鵡','翻譯','重播','崩潰','潮汐','自信','連登',
                  '神仙','守株待兔','曖昧','調情','狗公','外賣','中大','自修室','課外活動','節拍器','煙花','錯別字','係愛呀哈利','抖音','食雞','糖尿病','忍者','世風日下','記者招待會','化妝',
                  '分手','履歷','夢想','月台','貞子','朱克伯格','中藥','展覽','濾鏡','理論','譚仔','觀眾','桌球','素描','世界仔','大波妹','溫泉','騙案','手術室','大笨鐘','殘奧','光明磊落',
                  '地質學家','化石','變臉','瞬間移動','時間','心事台','未來人','抽屜','六合彩','莊家','成功','成龍','小龍女','急救','騎士','探險隊','歌劇','捉迷藏','迎新營','數獨','沙漠',
                  '見死不救','棒棒糖','花姐','肥仔','三步不出閨門','恐懼鬥室','鬧鬼','發燒','含羞草','肥絲大隻','波音','消費券','可口可樂','開源道','馬拉松','流浮山','砌圖','珍珠',
                  '長腳蟹','中秋節','端午節','聖誕節','萬聖節','勞動節','元宵節','截碼','狼人','Avalon','梅林','派西','騎士','特務','連環殺手','私家車','電動車','女學生','連登仔','人妻','熟女','紋身',
                  '重口味','麻辣','耶穌','佛祖','觀音','阿波羅','洗手間','去廁所','洗手','心急如焚','刮目相看','玉石俱焚','妲己','紂王','哪吒','孫悟空','豬八戒','唐三藏','沙僧','夠鐘',
                  '考試','加班','射波','爽膚水','搓手液','濕紙巾','微波爐','懶人包','掃描器','電鋸','摺凳','河馬','尿袋','菲林','曝光','光圈','快門',
                  '和服','斷食','熱狗','乳酪','貝果','司康','拉麵','宵夜','雞煲','雞排','糖醋肉','三色豆','四方果','帆立貝','厚多士',
                  '片皮鴨','甜不辣','蛋白粉','蛋包飯','部隊鍋','醬油蟹','佛跳牆','車仔麵','茶碗蒸','溏心蛋','和尚跳海','粟米肉磚','特特多麻',
                  '顱內高潮','仙人跳','蒲精','姣婆','媽寶','偷食','捉姦','偷拍','早洩','電子雞','蘭桂坊','打飛機','帝女花','金剛圈','卡卡西','Serrini',
                  '林家謙','東方昇','姜濤','Aimer','Yoasobi','米津玄師','新垣結衣','星野源','全民造星','歡樂馬介休','動物傳心師','選擇困難症','過度活躍症',
                  '情緒勒索','公主病','姆明','狼人殺','大電視','超級無敵搭錯線','空中瑜伽','多人運動','玉莖重生','印度神油','海龜湯','飛鵝山','星林居','茶餐廳',
                  '過山車','放題','蘋果','麻雀','武肺','阿仙奴','曼聯','車路士','防疫','廢老','小粉紅','躺平','石徑','露營','守宮','絕育','領養','塑膠','收兵',
                  '中出','口爆','顏射','龍舟掛鼓','夢遊','欺凌','移民','凌晨機','札幌','加拿大','林作','殯儀館','聖鬥士','算命','蹓冰','滑板','利息','彩蛋','表情',
                  '竹葉青','星期五','青少年','日蝕','冰河世紀','侏儸紀','大理石','琥珀','龍虎豹','羽毛球','智能家居','木蚤','鋤大DEE','拗柴','望夫石','乳齒','跳樓機','青藏高原',
                  '青花瓷','蒜頭','維京人','地中海','中東','李家超','地厚天高','梁天琦','痙攣','觀塘','左口魚','正手抽撃','賭場','神燈','燈神','水炮車','躁鬱症','思覺失調症',
                  '憂鬱症','強迫症','癌症','心臟病','亞氏保加症','黃藥師','歐陽鋒','洪七公','降龍十八掌','布丁燒','涼粉','魚滑','木瓜','牛肉麵','蒜泥白肉','急屎','潑水節','激光脫毛',
                  '人民幣','唐樓','生化危機','市集','空氣瀏海','冶癒系','濕疹','敏感肌','名牌','街舞','廣場舞','跳舞群組','激素','粟米肉粒飯','豆腐火腩飯','黯然銷魂飯',
                  '騎馬','秘撈','百日宴','強積金','郵費','文青','健身','啞鈴','水晶','滑梯','國安法','智慧齒','指南針','地圖','護目鏡','電話粥','藍牙耳機','子宮頸癌','愛滋病',
                  '維生素','乾癬','新陳代謝','高質','抽脂','整容','脫髮','禿頭','光療甲','大蛇屙尿','奶罩','跳樓 ','燒炭 ','安樂死 ','自殺永別','唐三藏','大肚婆','大眼雞','屎塔蓋','巨龍',
                  '撚狗','毛毛蟲','伊貝','炒飯','思覺失調','賤種','捐血','性病','吊頸 ','跳海','連登 ','高登 ','海洋公園','迪士尼樂園', '環球影城 ','天安門 ','太古廣場','mk妹',
                  '奪命狂呼', '毒撚', '洗剪吹', '利物浦''摩洛哥', '吉隆坡', '宣明會', '六月飛霜', '青春頌',
                  '油尖旺金毛玲', '孤單心事 ', 'ChiKaWa ', '小八 ', '兔兔 ', '芙莉蓮 ','曼城', '艾連', '進擊的巨人', '恐懼', '靈魂', '社畜', '失眠', '東方昇', '澳洲', '雙子塔', '萬里長城',
                  '林鄭月娥', '小海白', 'Mario', '路飛', '嗚人', '星之卡比', '比卡超', '三色豆', '咖啡', '楊枝甘露',
                  '杜奧巴', '保險狗', '基金佬', '美容雞', '機師', '紅十字會', 'JFFT', '貓', '狗 ', '沙龍',
                  '蘇格蘭場非工業用國際線路自動溶雪16Valve風油軑大包圍連鐳射彩色洗衣乾衣腐蝕性氣墊毛筆',"射箭", "田徑", "羽毛球", "籃球", "拳擊", "劍擊", "足球", "高爾夫", "體操", "手球", "曲棍球", "柔道", "射擊", "桌球", "跆拳道", "網球", "三項鐵人", "排球", "舉重", "棒球", "空手道", "滑板", "衝浪", "米爺", "米講風良話", "音樂擂台", "紅線計劃", "心事台", "時事台", "娛樂台", "JFFT", "YT大哥", "許賢", "拆彈專家", "玩轉腦朋友", "壞蛋獎門人", "海關戰線", "九龍城寨", "排球少年", "妖精的尾巴", "談判專家", "飯氣攻心",'張蔓姿', '玩轉腦朋友','Mirror', 'Facebook', '電話禁極刀', '葉佬', '米高佐敦',
                  '特朗普''美斯'"督察","設計師", "中藥配劑員", "巴士司機", "電子工程師", "工程技術員", "消防員", "酒店房務員", "騎師", "按摩師", "救護員", "寵物美容師", "飛行員", "泥水師傅", "放射師", "安全督導員", "裁縫", "倉務文員", "精算師", "航空通訊員", "生物學家", "屋宇測量師", "推拿師", "自然護理主任", "牙醫", "醫生", "翻譯員", "法醫", "視光師", "藥劑師", "獸醫", "新聞節目主播", "演員", "建築師", "編劇", "旅遊記者", "美容師", "貨運主任", "調酒師", "美容顧問", "中醫", "懲教主任", "營養師", "健身教練", "保安員", "髮型師", "保險從業員", "講師", "圖書館主任", "護士", "物理治療師", "警員", "核數師",]


    rs = random.sample(spell, 4)
    # Create the keyboard
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(rs[0],callback_data=f'rs_{rs[0]}'), InlineKeyboardButton(rs[1],callback_data=f'rs_{rs[1]}')],
        [InlineKeyboardButton(rs[2],callback_data=f'rs_{rs[2]}'), InlineKeyboardButton(rs[3],callback_data=f'rs_{rs[3]}')]
    ])

    # 村長選擇咒語
    await context.bot.send_message(
        chat_id=data[group_id]['村長'].id,
        text="請選擇咒語！",
        reply_markup=keyboard
    )
async def abc(update, context, group_id, user):
    print('a')
    await context.bot.send_message(
        chat_id=data[group_id]['先知'].id,
        text=f"咒語is{data[group_id]['spell']} ！"
    )
    print('b')
    for p in data[group_id]['狼人']:
        await context.bot.send_message(
            chat_id=p.id,
            text=f"咒語is{data[group_id]['spell']} ！"
        )
    print(context)


    # 判斷角色並發送PM
    await context.bot.send_message(
        chat_id=data[group_id]['村長'].id,
        text=f"你係村長，你既任務係主持大局！\n"
            f"如果你係先知村長，你既任務係主持大局既同時提示村民估到咒語，不過比壞人捉到你就輸喇！\n"
            f"如果你係狼村長，你既任務係主持大局既同時搞搞震，你可以比假提示，阻止村民估到答案！"
    )
    await context.bot.send_message(
        chat_id=data[group_id]['先知'].id,
        text=f"你係先知，你既任務提示村民估到咒語，不過比壞人捉到你就輸喇！"
    )
    for p in data[group_id]['狼人']:  # '狼人'
        await context.bot.send_message(
        chat_id=p.id,
        text=f"你係狼人，你的任務是搞搞震，阻止村民估到答案！"
    )
    for p in data[group_id]['村民']:  # '廢村'
        await context.bot.send_message(
        chat_id=p.id,
        text='你係廢村,你既任務係估到咒語！'
    )


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.message.chat.id
    user = update.message.from_user

    data[group_id]['players']['asks'] = 20
    if data[group_id]['players']['asks'] <= 0:
        await update.message.reply_text("你已經冇得問問題啦！")
        return

    if players not in data[group_id]['players']:
        await update.message.reply_text("你冇份玩,米嘈拉！") #冇玩既人輸入command
        return

    question = update.message.text.replace("/ask", "").strip()  #問題
    if not question:  # 檢查問題是否為空
        await update.message.reply_text("請輸入問題！")
        return


async def hints(update, context, group_id, user):  # 村長用鍵盤
    await context.bot.send_message(
        chat_id=data[group_id]['村長'].id,
        text="請選擇提示！",
        keyboard=InlineKeyboardMarkup[
            [InlineKeyboardButton("是", callback_data='村長話是！')],
            [InlineKeyboardButton("否", callback_data='村長話否！')],
            [InlineKeyboardButton("問號", callback_data='村長話唔清楚！')],
            [InlineKeyboardButton("差很遠", callback_data='村長話媽打媽打，你還差得遠呢！')],
            [InlineKeyboardButton("接近", callback_data='村長話接近！')],
            [InlineKeyboardButton("勁中", callback_data='村長話勁中！')]
        ])


answer = ['spell']
async def ans_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.message.chat.id
    user = update.message.from_user
    players = data[group_id]['players']
    ans = update.message.text.replace("/ans", "").strip()  # 答案

    if players not in data[group_id]['players']:
        await update.message.reply_text("你冇份玩,米嘈拉！")
        return

    answer = update.message.text.replace("/ans", "").strip()  # 答案
    if not ans:  # 檢查答案是否為空
        await update.message.reply_text("請輸入答案！")
        return

    await update.message.reply_text(f"你問嘅答案係: {ans}")  #Tag村長

    if answer.lower() == query_data['spell'].lower():
        # 玩家答對，村民陣營獲勝
        await update.message.reply_text(f"恭喜你答啱啦！答案就係「{answer}」！村民陣營獲勝！")
        # 這裡可以加入遊戲結束後的處理，例如重置遊戲狀態
    else:
        return

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.message.chat.id
    await update.message.reply_text(
        f"{data[group_id]['村長']} 的角色是 村長\n"
        f"{data[group_id]['先知']} 的角色是 先知\n"
        f"{data[group_id]['狼人']} 的角色是 狼人\n"
    )
    if group_id in data:
        data.pop(group_id)


async def rule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):     #Done
    await update.message.reply_text('遊戲角色分別有村長、狼人、先知及村民，\n'
                                    '遊戲開始時抽選一人做村長，並指派陣營（村長有機會是狼人或先知)'
                                    '，其後再分配角色。\n當遊戲人戲超過８人時，將會加入第二位狼人。\n'
                                    '在遊戲結束時，如咒語被好人陣營估中，狼人可以分別吉一位玩家，\n'
                                    '如該玩家為先知，即壞人獲勝。\n'
                                    '遊戲一共限時１０分鐘，\n'
                                    '各玩家分別透過輸入/ask 向村長獲得資訊 輸入/ans 估咒語\n'
                                    '，村長根據提問，分別點選\n'
                                    '是， 否， 問號， 差很多 及 接近 合共２０次機會\n'
                                    '，以提示或阻止好人估中如村民陣營未能於限時內找到正確答案或用完提示機會，即狼人陣營獲勝。\n'
                                    '如村民陣營估中咒語，狼人無法找到先知，即村民陣營獲勝。')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('你30歲人都無女朋友一定好有錢了 by檸檬頭')
    group_id = update.message.chat.id
    if group_id not in data:
        return
    players_name = [p.first_name for p in data[group_id]['players']]
    text = (f"玩家:{','.join(players_name)}")
    await context.bot.send_message(group_id, text)
   # Respones


async def y_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.message.chat.id
    user = update.message.from_user
    reply_message = update.message.reply_to_message
    if group_id not in data:
        return
    if not data[group_id]['started']:
        return
    if user != data[group_id]['村長']:
        return
    if reply_message:
        data[group_id]['yn'] += 1
        print('yn', data[group_id]['yn'])
        if data[group_id]['yn'] >= 36:
            context.bot.send_message(group_id, '36!')

async def n_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.message.chat.id
    user = update.message.from_user
    reply_message = update.message.reply_to_message
    print(reply_message)
    if group_id not in data:
        return
    if not data[group_id]['started']:
        return
    if user != data[group_id]['村長']:
        return
    if reply_message:
        data[group_id]['yn'] += 1
        print('yn', data[group_id]['yn'])
        if data[group_id]['yn'] >= 36:
            context.bot.send_message(group_id, '36!')


async def question_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.message.chat.id
    user = update.message.from_user
    reply_message = update.message.reply_to_message
    print(reply_message)
    if group_id not in data:
        return
    if not data[group_id]['started']:
        return
    if user != data[group_id]['村長']:
        return
    if reply_message:
        data[group_id]['?'] += 1
        if data[group_id]['?'] >= 10:
            context.bot.send_message(group_id, '10!')


def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'Hey there!'
    if '依加幾點' in processed:
        return '又夠鐘食藥'
    if 'i love banana' in processed:
        return '含我條蕉啦!'
    return random.sample(金句,1)[0]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}:"{text}"')
    if message_type =='group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print('Bot:',response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update{update} caused error {context.error}')



if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    data = {}  # dict
    print('fff')
    #Commands
    app.add_handler(CommandHandler('Start', start_command))
    app.add_handler(CommandHandler('rule', rule_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('join', join_command))
    app.add_handler(CommandHandler('new', new_command))
    app.add_handler(CommandHandler('stop', stop_command))
    app.add_handler(CommandHandler('flee', flee_command))
    app.add_handler(CommandHandler('ask', ask_command))
    app.add_handler(CommandHandler('ans', ans_command))
    app.add_handler(CommandHandler('y', y_command))
    app.add_handler(CommandHandler('n', n_command))
    app.add_handler(CommandHandler('qq', question_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    #app.add_error_handler(error)

    #Callback
    app.add_handler(CallbackQueryHandler(callback))

    #Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=0.1)

