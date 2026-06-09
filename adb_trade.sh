#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 ADB Mode ဖြင့် Bybit Automation စတင်နေပါပြီ..."

# ၁။ Bybit App ကို အလိုအလျောက် လှမ်းဖွင့်ခြင်း (Package Name ဖြင့် ခေါ်ခြင်း)
adb shell monkey -p com.bybit.app -c android.intent.category.LAUNCHER 1

# App ပွင့်လာအောင် ၅ စက္ကန့် စောင့်ပါ
sleep 5

# ၂။ Spot Trading Tab ရှိမယ့်နေရာကို နှိပ်ခြင်း 
# (ဥပမာ- စကရင်အောက်ခြေ အလယ်ဗဟို X=540, Y=2200 ဝန်းကျင် - သင့်ဖုန်း screen size အလိုက် ပြောင်းပေးရပါမယ်)
echo "🎯 Spot Tab ကို နှိပ်နေပါသည်..."
adb shell input tap 540 2200
sleep 2

# ၃။ 'Buy' ခလုတ်နေရာကို နှိပ်ခြင်း (ဥပမာ- X=250, Y=800)
echo "🎯 Buy ခလုတ်ကို နှိပ်နေပါသည်..."
adb shell input tap 250 800
sleep 1

# ၄။ ရိုက်ထည့်မည့် အကွက် (Amount Box) ကို နှိပ်ခြင်း (ဥပမာ- X=300, Y=1100)
echo "🎯 ပမာဏရိုက်ထည့်မည့် အကွက်ကို နှိပ်နေပါသည်..."
adb shell input tap 300 1100
sleep 1

# ၅။ ကီးဘုတ်ကနေ ဝယ်ယူမယ့် ပမာဏကို ရိုက်ထည့်ခြင်း (ဥပမာ- 10 USDT ဖိုး)
echo "⌨️ ဝယ်ယူမည့် ပမာဏ ရိုက်ထည့်နေပါသည်..."
adb shell input text "10"
sleep 1

# ၆။ နောက်ဆုံး 'Buy BTC' (သို့မဟုတ် ကုန်သွယ်မည့်ဒင်္ဂါး) အတည်ပြုခလုတ်ကြီးကို နှိပ်ခြင်း (ဥပမာ- X=500, Y=1500)
echo "🚀 အော်ဒါ အတည်ပြုချက် ခလုတ်ကို နှိပ်လိုက်ပါပြီ!"
adb shell input tap 500 1500

echo "✅ ADB Trade Process ပြီးဆုံးပါပြီ။"

#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 ADB Mode ဖြင့် Bybit Automation စတင်နေပါပြီ..."

# ၁။ Bybit App ကို အလိုအလျောက် လှမ်းဖွင့်ခြင်း (Package Name ဖြင့် ခေါ်ခြင်း)
adb shell monkey -p com.bybit.app -c android.intent.category.LAUNCHER 1

# App ပွင့်လာအောင် ၅ စက္ကန့် စောင့်ပါ
sleep 5

# ၂။ Spot Trading Tab ရှိမယ့်နေရာကို နှိပ်ခြင်း 
# (ဥပမာ- စကရင်အောက်ခြေ အလယ်ဗဟို X=540, Y=2200 ဝန်းကျင် - သင့်ဖုန်း screen size အလိုက် ပြောင်းပေးရပါမယ်)
echo "🎯 Spot Tab ကို နှိပ်နေပါသည်..."
adb shell input tap 540 2200
sleep 2

# ၃။ 'Buy' ခလုတ်နေရာကို နှိပ်ခြင်း (ဥပမာ- X=250, Y=800)
echo "🎯 Buy ခလုတ်ကို နှိပ်နေပါသည်..."
adb shell input tap 250 800
sleep 1

# ၄။ ရိုက်ထည့်မည့် အကွက် (Amount Box) ကို နှိပ်ခြင်း (ဥပမာ- X=300, Y=1100)
echo "🎯 ပမာဏရိုက်ထည့်မည့် အကွက်ကို နှိပ်နေပါသည်..."
adb shell input tap 300 1100
sleep 1

# ၅။ ကီးဘုတ်ကနေ ဝယ်ယူမယ့် ပမာဏကို ရိုက်ထည့်ခြင်း (ဥပမာ- 10 USDT ဖိုး)
echo "⌨️ ဝယ်ယူမည့် ပမာဏ ရိုက်ထည့်နေပါသည်..."
adb shell input text "10"
sleep 1

# ၆။ နောက်ဆုံး 'Buy BTC' (သို့မဟုတ် ကုန်သွယ်မည့်ဒင်္ဂါး) အတည်ပြုခလုတ်ကြီးကို နှိပ်ခြင်း (ဥပမာ- X=500, Y=1500)
echo "🚀 အော်ဒါ အတည်ပြုချက် ခလုတ်ကို နှိပ်လိုက်ပါပြီ!"
adb shell input tap 500 1500

echo "✅ ADB Trade Process ပြီးဆုံးပါပြီ။"

