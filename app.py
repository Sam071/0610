from flask import Flask, render_template, request
import yfinance as yf
import os

app = Flask(__name__)

# 1. 首頁
@app.route('/')
def index():
    return render_template('index.html')

# 2. 股票查詢頁面
@app.route('/stock', methods=['GET', 'POST'])
def stock():
    stock_data = None
    ticker = None
    error_msg = None
    
    if request.method == 'POST':
        ticker = request.form.get('ticker', '').upper()
        if ticker:
            try:
                # 預設查詢台灣股票需要加 .TW，例如 2330.TW
                # 如果使用者沒輸入，且是純數字，幫他補上 .TW
                if ticker.isdigit():
                    search_ticker = f"{ticker}.TW"
                else:
                    search_ticker = ticker
                    
                tk = yf.Ticker(search_ticker)
                info = tk.info
                history = tk.history(period="1d")
                
                if not history.empty:
                    stock_data = {
                        'name': info.get('longName', ticker),
                        'price': round(history['Close'].iloc[-1], 2),
                        'open': round(history['Open'].iloc[-1], 2),
                        'high': round(history['High'].iloc[-1], 2),
                        'low': round(history['Low'].iloc[-1], 2),
                        'volume': int(history['Volume'].iloc[-1])
                    }
                else:
                    error_msg = "找不到該股票資料，請檢查代號是否正確（台股請輸入如 2330）"
            except Exception as e:
                error_msg = f"讀取資料時發生錯誤: {str(e)}"
                
    return render_template('stock.html', stock_data=stock_data, ticker=ticker, error_msg=error_msg)

# 3. 天氣預報與交通推薦
@app.route('/weather', methods=['GET', 'POST'])
def weather():
    weather_info = None
    city = None
    
    # 模擬天氣與交通推薦邏輯
    city_data = {
        '台北': {'temp': '26°C', 'condition': '陰有雨', 'traffic': '下雨天容易塞車，強烈建議搭乘台北捷運（MRT），省時又安全！'},
        '台中': {'temp': '29°C', 'condition': '晴時多雲', 'traffic': '天氣晴朗，推薦騎乘 YouBike 或搭乘台中公車、捷運暢遊市區。'},
        '高雄': {'temp': '31°C', 'condition': '豔陽天', 'traffic': '天氣炎熱，建議搭乘高雄輕軌或捷運，並做好防曬準備。'}
    }
    
    if request.method == 'POST':
        city = request.form.get('city')
        if city in city_data:
            weather_info = city_data[city]
            
    return render_template('weather.html', weather_info=weather_info, city=city)

# 4. 台北美食介紹
@app.route('/food')
def food():
    # 靜態美食資料陣列
    restaurants = [
        {"name": "鼎泰豐 (信義店)", "type": "中式點心", "desc": "享譽國際的小籠包，皮薄汁多，服務也是一流水準。", "mrt": "東門站"},
        {"name": "大稻埕 慈聖宮豬腳麵線", "type": "傳統小吃", "desc": "老台北人的原汁原味，清燉豬腳湯頭濃郁，肉質 Q 彈。", "mrt": "大橋頭站"},
        {"name": "詹記麻辣火鍋", "type": "麻辣火鍋", "desc": "超人氣排隊名店，鴨血滑嫩如豆腐，是台北必吃麻辣鍋。", "mrt": "六張犁站"},
        {"name": "饒河街夜市 福州世祖胡椒餅", "type": "夜市小吃", "desc": "現烤出爐的外皮酥脆，內餡肉汁飽滿、胡椒香氣十足。", "mrt": "松山站"}
    ]
    return render_template('food.html', restaurants=restaurants)

if __name__ == '__main__':
    # Render 部署需要讀取環境變數的 PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
