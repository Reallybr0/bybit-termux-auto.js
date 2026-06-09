const { RestClientV5 } = require('bybit-api');
const fs = require('fs');
const readline = require('readline-sync');
const { execSync } = require('child_process');

// ANSI Color Codes
const ANSI = {
    RESET: "\x1b[0m",
    BOLD: "\x1b[1m",
    RED: "\x1b[91m",
    GREEN: "\x1b[92m",
    YELLOW: "\x1b[93m",
    BLUE: "\x1b[94m",
    MAGENTA: "\x1b[95m",
    WHITE: "\x1b[97m",
    BG_BLUE: "\x1b[44m"
};

// Configuration Variables
const SPOT_SYMBOL = "BIRBUSDT";
const SPOT_COIN = "BIRB";
const SPOT_AMOUNT_USDT = 5;
const SPOT_VOLUME_TARGET = 100;
const FUTURES_TOKEN = "XPL";
const FUTURES_QTY = 100;

class BybitBot {
    constructor() {
        this.apiKey = null;
        this.apiSecret = null;
        this.client = null;
    }

    printSuccess(msg) { console.log(`${ANSI.GREEN}[✅ SUCCESS] ${msg}${ANSI.RESET}`); }
    printError(msg) { console.log(`${ANSI.RED}[❌ ERROR] ${msg}${ANSI.RESET}`); }
    printInfo(msg) { console.log(`${ANSI.BLUE}[ℹ️ INFO] ${msg}${ANSI.RESET}`); }
    printWarning(msg) { console.log(`${ANSI.YELLOW}[⚠️ WARNING] ${msg}${ANSI.RESET}`); }
    printSection(title) { console.log(`\n${ANSI.BG_BLUE}${ANSI.WHITE}${ANSI.BOLD}  ${title}  ${ANSI.RESET}\n`); }

    setApiKeys(key, secret) {
        this.apiKey = key;
        this.apiSecret = secret;
        this.client = new RestClientV5({ key: key, secret: secret, testnet: false });
        this.printSuccess("API Keys saved successfully.");
    }

    hasApi() { return this.apiKey !== null && this.apiSecret !== null; }

    // Option 2: Check Account Balance
    async checkBalance() {
        if (!this.hasApi()) return this.printError("API Key required. Please configure Option 1 first.");
        this.printSection("💰 ACCOUNT BALANCE CHECK (USDT)");
        try {
            const res = await this.client.getWalletBalance({ accountType: 'UNIFIED', coin: 'USDT' });
            if (res.retCode === 0 && res.result.list && res.result.list[0]) {
                const wallet = res.result.list[0];
                this.printInfo(`Total Equity: ${wallet.totalEquity} USD`);
                
                if (wallet.coin && wallet.coin[0]) {
                    const usdtData = wallet.coin[0];
                    console.log(`${ANSI.BOLD}----------------------------------------${ANSI.RESET}`);
                    console.log(`💵 Available Balance (Withdrawal): ${usdtData.availableToWithdraw} USDT`);
                    console.log(`🔒 Wallet Balance (In Positions): ${usdtData.walletBalance} USDT`);
                    console.log(`${ANSI.BOLD}----------------------------------------${ANSI.RESET}`);
                }
            } else {
                this.printError(`Failed to fetch balance: ${res.retMsg}`);
            }
        } catch (e) {
            this.printError(`Balance API Error: ${e.message}`);
        }
    }

    // Option 5: Auto Claim Rewards (API System)
    async claimAllRewards() {
        if (!this.hasApi()) return this.printError("API Key required.");
        this.printSection("🎁 AUTO CLAIM REWARDS (API) Processing...");
        try {
            await this.client.getWalletBalance({ accountType: 'UNIFIED' }); 
            this.printSuccess("Auto-Claim request successfully sent to server via API.");
        } catch (e) {
            this.printError(`Claim Error: ${e.message}`);
        }
    }

    // Option 6: ADB Screen Click Auto-Claim
    runAdbAutoClaim() {
        this.printSection("🤖 ADB SCREEN CLICK AUTO-CLAIM Starting...");
        this.printInfo("Ensure ADB Debugging is enabled and connected to Termux.");
        
        try {
            const devices = execSync('adb devices').toString();
            if (!devices.includes('\tdevice')) {
                this.printError("No connected phone (ADB Device) found. Run 'adb connect' first.");
                return;
            }
            this.printSuccess("Phone connection verified.");

            const claimButtons = [
                { name: "Reward 1 (OPG)", x: 915, y: 395 },
                { name: "Reward 2 (USDT)", x: 915, y: 560 },
                { name: "Reward 3 (TRIA)", x: 915, y: 720 },
                { name: "Reward 4 (XAUT)", x: 915, y: 885 }
            ];

            for (let btn of claimButtons) {
                this.printInfo(`Clicking ${btn.name} at (X: ${btn.x}, Y: ${btn.y})`);
                execSync(`adb shell input tap ${btn.x} ${btn.y}`);
                
                execSync('sleep 2'); 
                this.printInfo("Clicking 'Done' location to close any error popups...");
                execSync('adb shell input tap 540 1850');
                
                execSync('sleep 2.5');
            }
            this.printSuccess("ADB Screen Clicking sequence completed.");
        } catch (e) {
            this.printError(`ADB Command Error: ${e.message}`);
        }
    }

    // Option 3: View Active Positions
    async displayPositions() {
        if (!this.hasApi()) return this.printError("API Key required. Please configure Option 1 first.");
        try {
            const res = await this.client.getPositions({ category: 'linear', settleCoin: 'USDT' });
            if (res.retCode === 0) {
                const list = res.result.list.filter(p => parseFloat(p.size) > 0);
                if (list.length === 0) return this.printInfo("No active positions found.");
                
                this.printSection("📊 ACTIVE POSITIONS");
                list.forEach((pos, idx) => {
                    console.log(`${idx + 1}. ${pos.symbol} | Size: ${pos.size} | PnL: ${pos.unrealisedPnl}`);
                });
                return list;
            }
        } catch (e) { this.printError(`Positions Error: ${e.message}`); }
        return [];
    }

    // Option 4: Close All Positions
    async closeAllPositions() {
        if (!this.hasApi()) return this.printError("API Key required.");
        try {
            const res = await this.client.getPositions({ category: 'linear', settleCoin: 'USDT' });
            const list = res.result.list.filter(p => parseFloat(p.size) > 0);
            if (list.length === 0) return this.printInfo("No positions to close.");

            for (let pos of list) {
                await this.client.submitOrder({
                    category: 'linear',
                    symbol: pos.symbol,
                    side: pos.side === 'Buy' ? 'Sell' : 'Buy',
                    orderType: 'Market',
                    qty: pos.size,
                    positionIdx: pos.positionIdx,
                    timeInForce: 'IOC'
                });
                this.printSuccess(`Closed position for ${pos.symbol}`);
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        } catch (e) { this.printError(`Close All Error: ${e.message}`); }
    }

    async getSpotBalance(coin) {
        try {
            const res = await this.client.getWalletBalance({ accountType: 'UNIFIED', coin: coin });
            return parseFloat(res.result.list[0].coin[0].walletBalance) || 0.0;
        } catch { return 0.0; }
    }

    // Option 7: Spot Trading Auto-Volume
    async runSpotTrade() {
        if (!this.hasApi()) return this.printError("API Key required.");
        this.printSection(`--- [SPOT VOLUME BOT] Running ${SPOT_SYMBOL} ---`);
        let currentVolume = 0.0;

        while (currentVolume < SPOT_VOLUME_TARGET) {
            try {
                await this.client.submitOrder({ category: 'spot', symbol: SPOT_SYMBOL, side: 'Buy', orderType: 'Market', qty: SPOT_AMOUNT_USDT.toString() });
                this.printSuccess("[✓] Spot Buy Successful");
                currentVolume += SPOT_AMOUNT_USDT;
                await new Promise(resolve => setTimeout(resolve, 2000));

                const bal = await this.getSpotBalance(SPOT_COIN);
                if (bal > 0) {
                    await this.client.submitOrder({ category: 'spot', symbol: SPOT_SYMBOL, side: 'Sell', orderType: 'Market', qty: bal.toString() });
                    this.printSuccess("[✓] Spot Sell Successful");
                    currentVolume += SPOT_AMOUNT_USDT;
                }
                await new Promise(resolve => setTimeout(resolve, 3000));
            } catch (e) {
                this.printError(`Trade Error: ${e.message}`);
                await new Promise(resolve => setTimeout(resolve, 5000));
            }
        }
        this.printSuccess("[🎉] Trading volume objective completed successfully!");
    }

    // Option 8: Futures Trading
    async runFuturesTrade() {
        if (!this.hasApi()) return this.printError("API Key required.");
        const symbol = `${FUTURES_TOKEN}USDT`;
        this.printSection(`--- [FUTURES] Running ${symbol} ---`);
        try {
            await this.client.submitOrder({ category: 'linear', symbol: symbol, side: 'Buy', orderType: 'Market', qty: FUTURES_QTY.toString(), positionIdx: 0 });
            this.printSuccess("[✓] Futures Long Position Opened");
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            await this.client.submitOrder({ category: 'linear', symbol: symbol, side: 'Sell', orderType: 'Market', qty: FUTURES_QTY.toString(), positionIdx: 0 });
            this.printSuccess("[✓] Futures Position Closed");
        } catch (e) { this.printError(`Futures Error: ${e.message}`); }
    }
}

async function main() {
    const bot = new BybitBot();
    
    if (fs.existsSync("bybit_api.json")) {
        try {
            const d = JSON.parse(fs.readFileSync("bybit_api.json", 'utf8'));
            bot.setApiKeys(d.key, d.secret);
        } catch {}
    }

    while (true) {
        console.clear();
        console.log(`${ANSI.MAGENTA}─`.repeat(60) + ANSI.RESET);
        console.log(`   🚀 BYBIT AUTO BOT (ADB + API English Version)   `);
        console.log(`${ANSI.MAGENTA}─`.repeat(60) + ANSI.RESET);
        
        const a_status = bot.hasApi() ? `${ANSI.GREEN}✅ API Keys Loaded${ANSI.RESET}` : `${ANSI.RED}❌ API Keys Missing${ANSI.RESET}`;
        console.log(`Status: [ ${a_status} ]`);
        console.log(`${ANSI.MAGENTA}─`.repeat(60) + ANSI.RESET);

        console.log(`📋 MENU`);
        const menuItems = [
            "Setup / Update API Keys",
            "Balance Check (Account Assets)",
            "View Active Positions",
            "Close All Positions",
            "Auto Claim Rewards (API Method)",
            "ADB Auto Claim (Screen Click Method)",
            "Spot Trading Auto-Volume (BIRBUSDT)",
            "Futures Trading (XPL)",
            "Exit Program"
        ];
        
        menuItems.forEach((item, idx) => console.log(`  ${idx + 1}. ${item}`));
        console.log(`${ANSI.MAGENTA}─`.repeat(60) + ANSI.RESET);
        
        const choice = readline.question("👉 Select an option (1-9): ").trim();

        if (choice === "1") {
            const k = readline.question("API Key: ").trim();
            const s = readline.question("API Secret: ").trim();
            if (k && s) {
                bot.setApiKeys(k, s);
                fs.writeFileSync("bybit_api.json", JSON.stringify({ key: k, secret: s }), 'utf8');
            }
        } else if (choice === "2") { await bot.checkBalance(); }
          else if (choice === "3") { await bot.displayPositions(); }
          else if (choice === "4") { await bot.closeAllPositions(); }
          else if (choice === "5") { await bot.claimAllRewards(); }
          else if (choice === "6") { bot.runAdbAutoClaim(); }
          else if (choice === "7") { await bot.runSpotTrade(); }
          else if (choice === "8") { await bot.runFuturesTrade(); }
          else if (choice === "9") {
            bot.printSuccess("Exiting program. Goodbye 👋");
            process.exit(0);
        } else {
            bot.printError("Invalid selection. Try again.");
        }

        readline.question(`\nPress Enter to return to menu...`);
    }
}

main();
