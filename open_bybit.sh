#!/bin/bash

# ANSI Color Codes (အရောင်အလှဆင်ခြင်း)
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}[ℹ️] Sending launch command to Bybit App...${NC}"
# ၁။ Bybit App ကို လှမ်းဖွင့်ခြင်း
adb shell monkey -p com.bybit.app -c android.intent.category.LAUNCHER 1

# ⏳ App ပွင့်ပြီး စာမျက်နှာ Reload ဖြစ်အောင် ၃၀ စက္ကန့် စောင့်ခြင်း
echo -e "${YELLOW}[⏳] App ပွင့်သွားပါပြီ။ Home Screen ပေါ်လာရန် 30 စက္ကန့် စောင့်ဆိုင်းနေပါသည်...${NC}"
sleep 30

# ၂။ ဗီဒီယိုအတိုင်း Rewards Hub ထဲသို့ ဝင်ရန် နှိပ်ခြင်း
echo -e "${BLUE}[🕹️] Step 1: Entering 'Rewards Hub'...${NC}"
adb shell input tap 180 460
echo -e "${YELLOW}[⏳] Rewards Hub Loading... 30 စက္ကန့် စောင့်ဆိုင်းနေပါသည်...${NC}"
sleep 30

# ၃။ ညာဘက်အပေါ်ထောင့်နားက "My Rewards" (စာအိတ်ပုံစံ) ကို နှိပ်ခြင်း
echo -e "${BLUE}[🕹️] Step 2: Clicking 'My Rewards' icon...${NC}"
adb shell input tap 830 115
echo -e "${YELLOW}[⏳] My Rewards Page Loading... 25 စက္ကန့် စောင့်ဆိုင်းနေပါသည်...${NC}"
sleep 25

# ၄။ သီးသန့် "Available" Tab ကို ရွေးချယ်နှိပ်ခြင်း
echo -e "${BLUE}[🕹️] Step 3: Clicking 'Available' Tab...${NC}"
adb shell input tap 290 170
echo -e "${YELLOW}[⏳] Available List Loading... 30 စက္ကန့် စောင့်ဆိုင်းနေပါသည်...${NC}"
sleep 30


# --- ၅။ ဆုလာဘ်များကို တစ်ခုချင်းစီ ကလစ်နှိပ်၍ Claim ခြင်း စနစ် ---
echo -e "${GREEN}[🚀] စတင်၍ ဆုလာဘ်များကို တစ်ခုချင်းစီ (ခွာပြီး) လှမ်းနှိပ်နေပါပြီ...${NC}"

# function တစ်ခုဆောက်ပြီး ပုံသေလုပ်ဆောင်ချက်ကို ပတ်ခိုင်းခြင်း (Code တိုသွားအောင်)
claim_reward_sequence() {
    local reward_num=$1
    local list_y=$2 # စာရင်းထဲက Claim ခလုတ်နေရာ

    echo -e "${PURPLE}--------------------------------------------------${NC}"
    echo -e "${BLUE}[🎁] ဆုလာဘ် (${reward_num}) ရဲ့ 'Claim' ခလုတ်ကို နှိပ်လိုက်သည်...${NC}"
    adb shell input tap 900 $list_y
    sleep 3 # စာမျက်နှာအောက်ခြေက Claim ခလုတ်ကြီး တက်လာရန် ခဏစောင့်ခြင်း

    echo -e "${BLUE}[🎯] အတွင်းထဲက အပြာရောင် 'Claim' ခလုတ်ကြီးကို ထပ်နှိပ်သည်...${NC}"
    adb shell input tap 540 1850
    sleep 3 # Error Popup တက်လာရန် ခဏစောင့်ခြင်း

    echo -e "${BLUE}[🛑] Error Popup ကို ပိတ်ရန် 'Done' ခလုတ်ကို နှိပ်သည်...${NC}"
    adb shell input tap 540 1850
    sleep 2

    echo -e "${BLUE}[↩️] စာရင်းထဲ ပြန်ရောက်ရန် ဘယ်ဘက်အပေါ်က 'Back' မျှားကို နှိပ်သည်...${NC}"
    adb shell input tap 70 115
    
    echo -e "${YELLOW}[⏳] သတ်မှတ်ချက်အတိုင်း 15 စက္ကန့် ခြားပြီးမှ နောက်တစ်ခုကို ဆက်သွားပါမည်...${NC}"
    sleep 15
}

# ဆုလာဘ် (၁) - ပထမဆုံး အတန်း
claim_reward_sequence "1" "410"

# ဆုလာဘ် (၂) - ဒုတိယ အတန်း
claim_reward_sequence "2" "580"

# ဆုလာဘ် (၃) - တတိယ အတန်း
claim_reward_sequence "3" "740"

# ဆုလာဘ် (၄) - စတုတ္ထ အတန်း
claim_reward_sequence "4" "910"

echo -e "${PURPLE}--------------------------------------------------${NC}"
echo -e "${GREEN}[🎉] ဗီဒီယိုထဲက လုပ်ဆောင်ချက်အတိုင်း တစ်ခုချင်းစီကို အချိန် Delay အတိအကျဖြင့် Claim ပြီးပါပြီ!${NC}"

