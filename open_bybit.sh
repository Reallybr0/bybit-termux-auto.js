#!/data/data/com.termux/files/usr/bin/bash

# ၁။ Bybit App ကို အလိုအလျောက် စတင်ဖွင့်လှစ်ခြင်း
echo "🔄 Bybit App ကို လှမ်းဖွင့်နေပါပြီ..."
adb shell monkey -p com.bybit.app -c android.intent.category.LAUNCHER 1
sleep 6 # App ပွင့်လာပြီး ကြော်ငြာ overlay တွေ ပျောက်သွားအောင် ၆ စက္ကန့် စောင့်ပေးပါမယ်

# ၂။ ဘယ်ဘက်အပေါ်ထောင့်က Profile ပုံကို နှိပ်ခြင်း
echo "👤 Profile ထဲသို့ ဝင်နေပါပြီ..."
adb shell input tap 75 75
sleep 3 # Profile Page ပွင့်လာအောင် စောင့်ခြင်း

# ၃။ Rewards Hub ခလုတ်ကို နှိပ်ခြင်း
echo "🎁 Rewards Hub ကို နှိပ်နေပါပြီ..."
adb shell input tap 700 450
sleep 5 # Rewards Hub Page က loaded ဖြစ်တာ နှေးတတ်လို့ ၅ စက္ကန့် စောင့်ခြင်း

# ၄။ My Rewards Tab ထဲသို့ ဝင်ခြင်း
echo "📂 My Rewards သို့ ကူးပြောင်းနေပါပြီ..."
adb shell input tap 620 160
sleep 4 # Rewards စာရင်း ပွင့်လာအောင် စောင့်ခြင်း

# ၅။ ပထမဆုံးအပေါ်ဆုံးက 'Claim' ခလုတ်ကို နှိပ်ခြင်း (6 OPG)
echo "💰 ပထမဆုံး Reward ကို Claim နှိပ်နေပါပြီ..."
adb shell input tap 920 170
sleep 4 # အောင်မြင်/မအောင်မြင် ပေါ့ပ်အပ်တက်လာတာကို စောင့်ခြင်း

# ၆။ ခလုတ်နှိပ်ပြီးနောက် တက်လာမည့် Overlay ပေါ့ပ်အပ်ကို ပိတ်ခြင်း (သို့) 'Done' နှိပ်ခြင်း
echo "✅ ပေါ့ပ်အပ်ကို ပိတ်နေပါပြီ..."
adb shell input tap 540 920 
sleep 2

echo "🎉 လုပ်ဆောင်ချက် အားလုံး ပြီးမြောက်ပါပြီ။"

