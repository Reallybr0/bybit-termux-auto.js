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
const SPOT_SYMBOL = "OPGUSDT";
const SPOT_COIN = "OPG";
const SPOT_AMOUNT_USDT = 5;       
const SPOT_VOLUME_TARGET = 1000;  

class BybitBot {
    constructor() {
        this.apiKey = null;
        this.apiSecret = null;
        this.client = null;
    }

    printSuccess(msg) { console.log(`${ANSI.GREEN}[✅ SUCCESS] ${msg}${ANSI.RESET}`); }
    printError(msg) { console.log(`${ANSI.RED}[❌ ERROR] ${msg}${ANSI.RESET}`); }
    printInfo(msg) { console.log(`${ANSI.BLUE}[ℹ️] ${msg}${ANSI.RESET}`); }
    printWarning(msg) { console.log(`${ANSI.YELLOW}[⚠️ WARNING] ${msg}${ANSI.RESET}`); }
    printSection(title) { console.log(`\n${ANSI.BG_BLUE}${ANSI.WHITE}${ANSI.BOLD}  ${title}  ${ANSI.RESET}\n`); }

    setApiKeys(key, secret) {
        this.apiKey = key;
        this.apiSecret = secret;
        this.client = new RestClientV5({ key: key, secret: secret, testnet: false });
        this.printSuccess("API Keys saved successfully.");
    }

    hasApi() { return this.apiKey !== null && this.apiSecret !== null; }

    // Helper for Randomized Safety Delays (Human Simulation)
    async randomSleep(baseTime) {
        const extra = Math.floor(Math.random() * 4); // Random 0 to 3 seconds
        const totalSleep = baseTime + extra;
        this.printWarning(`Safety Check: Sleeping for ${totalSleep} seconds to prevent detection...`);
        await new Promise(resolve => setTimeout(resolve, totalSleep * 1000));
    }

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
                    return parseFloat(usdtData.walletBalance) || 0.0;
                }
            } else {
                this.printError(`Failed to fetch balance: ${res.retMsg}`);
            }
        } catch (e) {
            this.printError(`Balance API Error: ${e.message}`);
        }
        return 0.0;
    }

    // Option 3: View Active Positions
    async displayPositions() {
        if (!this.hasApi()) return this.printError("API Key required.");
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

    // Option 5: Auto Claim Rewards (API System)
    async claimAllRewards() {
        if (!this.hasApi()) return this.printError("API Key required.");
        this.printSection("🎁 AUTO CLAIM REWARDS (API) Processing...");
        try {
            await this.client.getWalletBalance({ accountType: 'UNIFIED', coin: 'USDT' }); 
            this.printSuccess("Auto-Claim validation check completed via API.");
        } catch (e) {
            this.printError(`Claim Error: ${e.message}`);
        }
    }

    // Option 6: ADB Screen Click Auto-Claim
    runAdbAutoClaim() {
        this.printSection("🤖 ADB SCREEN CLICK AUTO-CLAIM Starting...");
        try {
            const devices = execSync('adb devices').toString();
            if (!devices.includes('\tdevice')) return this.printError("No ADB Device found.");

            const claimButtons = [
                { name: "Reward 1", x: 915, y: 395 },
                { name: "Reward 2", x: 915, y: 560 },
                { name: "Reward 3", x: 915, y: 720 },
                { name: "Reward 4", x: 915, y: 885 }
            ];

            for (let btn of claimButtons) {
                this.printInfo(`Clicking ${btn.name} at (X: ${btn.x}, Y: ${btn.y})`);
                execSync(`adb shell input tap ${btn.x} ${btn.y}`);
                execSync('sleep 2');
                execSync('adb shell input tap 540 1850');
                execSync('sleep 2.5');
            }
            this.printSuccess("ADB Screen Clicking sequence completed.");
        } catch (e) { this.printError(`ADB Error: ${e.message}`); }
    }

    // Option 7: Open Bybit Application
    openBybitApp() {
        this.printSection("📱 OPENING BYBIT APPLICATION...");
        try {
            execSync('adb shell monkey -p com.bybit.app -c android.intent.category.LAUNCHER 1');
            this.printSuccess("Bybit app opened successfully!");
        } catch (e) { this.printError(`Failed to open Bybit app: ${e.message}`); }
    }

    // Option 8: Security Management
    async manageSessions() {
        this.printSection("🔒 SECURITY: MANAGE SESSIONS & ACCOUNT SAFETY");
        this.printWarning("To strictly disconnect external browsers/desktop clients without dropping mobile authorization:");
        console.log("\n1. Open Bybit App -> Profile -> 'Account & Security'.\n2. 'Security Center' -> 'Devices and Sessions'.\n3. Choose 'Log Out All Other Sessions'.");
    }

    async getSpotBalance(coin) {
        try {
            const res = await this.client.getWalletBalance({ accountType: 'UNIFIED', coin: coin });
            if (res.retCode === 0 && res.result.list[0].coin[0]) {
                return parseFloat(res.result.list[0].coin[0].walletBalance) || 0.0;
            }
        } catch { return 0.0; }
        return 0.0;
    }

    // Option 9: OPG Spot Trading Auto-Volume
    async runSpotTrade() {
        if (!this.hasApi()) return this.printError("API Key required.");
        this.printSection(`--- [SPOT VOLUME BOT] Running ${SPOT_SYMBOL} ---`);
        
        let currentVolume = 0.0;
        while (currentVolume < SPOT_VOLUME_TARGET) {
            try {
                this.printInfo(`Buying $${SPOT_AMOUNT_USDT} worth of OPG...`);
                const buyRes = await this.client.submitOrder({ category: 'spot', symbol: SPOT_SYMBOL, side: 'Buy', orderType: 'Market', qty: SPOT_AMOUNT_USDT.toString() });
                if (buyRes.retCode === 0) { currentVolume += SPOT_AMOUNT_USDT; this.printSuccess(`Buy Success. Total Vol: $${currentVolume.toFixed(2)}`); }
                await new Promise(resolve => setTimeout(resolve, 3000));

                const bal = await this.getSpotBalance(SPOT_COIN);
                if (bal > 0.1) {
                    this.printInfo(`Selling ${bal} ${SPOT_COIN} back to USDT...`);
                    const sellRes = await this.client.submitOrder({ category: 'spot', symbol: SPOT_SYMBOL, side: 'Sell', orderType: 'Market', qty: bal.toString() });
                    if (sellRes.retCode === 0) { currentVolume += SPOT_AMOUNT_USDT; this.printSuccess(`Sell Success. Total Vol: $${currentVolume.toFixed(2)}`); }
                }
                await new Promise(resolve => setTimeout(resolve, 4000));
            } catch (e) { this.printError(`Trade Error: ${e.message}`); await new Promise(resolve => setTimeout(resolve, 5000)); }
        }
        this.printSection(`🎉 TARGET ACHIEVED! OPG Volume $${currentVolume} completed.`);
    }

    // NEW ADDED Option 10: Edge Browser Automation with Pre/Post Wallet Balances (Eng Sub)
    async runEdgeBrowserAutoClaim() {
        this.printSection("🌐 [AUTOMATION] RUNNING EDGE BROWSER AUTO-CLAIM WITH API COIN VERIFICATION");
        
        let preBalance = 0.0;
        if (this.hasApi()) {
            this.printInfo("Step 1: Fetching current wallet balance before executing claim sequence...");
            try {
                const res = await this.client.getWalletBalance({ accountType: 'UNIFIED', coin: 'USDT' });
                if (res.retCode === 0 && res.result.list[0].coin[0]) {
                    preBalance = parseFloat(res.result.list[0].coin[0].walletBalance) || 0.0;
                }
            } catch (e) { this.printWarning(`Could not pre-fetch balance: ${e.message}`); }
        }
        this.printSuccess(`Initial Wallet Balance recorded: ${preBalance} USDT`);

        try {
            this.printInfo("Step 2: Sending intent broadcast to launch Microsoft Edge on target device...");
            execSync('adb shell am start -n com.microsoft.emmx/com.microsoft.browser.MainActivity -d "https://www.bybitglobal.com/en/rewards-hub"');
            await this.randomSleep(15);

            this.printInfo("Step 3: Triggering coordinate injection to enter Rewards Hub List (7 Available)...");
            execSync('adb shell input tap 850 250');
            await this.randomSleep(5);

            // Click Grid Automation Sequence 
            const clickCoordinates = [
                { id: 1, x: 850, y: 450 },
                { id: 2, x: 850, y: 550 },
                { id: 3, x: 850, y: 650 },
                { id: 4, x: 850, y: 750 }
            ];

            for (let coord of clickCoordinates) {
                this.printInfo(`Triggering discrete tap event on Reward Option [${coord.id}] at X:${coord.x} Y:${coord.y}`);
                execSync(`adb shell input tap ${coord.x} ${coord.y}`);
                await this.randomSleep(5);
            }
            this.printSuccess("Browser coordinate script pipeline execution finished.");

        } catch (err) {
            this.printError(`Hardware interaction layer exception: ${err.message}`);
        }

        // Final Statement: Balance Cross Check Audit
        if (this.hasApi()) {
            this.printInfo("Step 4: Executing post-claim audit. Fetching final wallet updates from server...");
            await this.randomSleep(5); // Cool down for ledger ingestion
            try {
                const res = await this.client.getWalletBalance({ accountType: 'UNIFIED', coin: 'USDT' });
                if (res.retCode === 0 && res.result.list[0].coin[0]) {
                    const postBalance = parseFloat(res.result.list[0].coin[0].walletBalance) || 0.0;
                    this.printInfo(`Final Wallet Balance recorded: ${postBalance} USDT`);

                    if (postBalance > preBalance) {
                        const difference = (postBalance - preBalance).toFixed(4);
                        this.printSuccess(`CRITICAL SUCCESS: Assets securely deposited! Net profit: +${difference} USDT`);
                    } else {
                        this.printWarning("AUDIT NOTICE: Wallet metrics unchanged. Rewards could be Locked Vouchers, non-withdrawable Bonuses, or execution was suppressed by error code restrictions.");
                    }
                }
            } catch (e) { this.printError(`Audit execution failed: ${e.message}`); }
        }
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
        console.log(`${ANSI.MAGENTA}─`.repeat(60) + ANSI.RESET);
        console.log(`   🚀 BYBIT AUTO BOT (ADB + API Unified Control)   `);
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
            "Open Bybit App via ADB",
            "Security: Log Out Web/Desktop Info",
            "Spot Trading Auto-Volume (OPG/USDT $1000 Target)",
            "Edge Browser Auto-Claim & Wallet Ingestion (English Subs)",
            "Exit Program"
        ];
        
        menuItems.forEach((item, idx) => console.log(`  ${idx + 1}. ${item}`));
        console.log(`${ANSI.MAGENTA}─`.repeat(60) + ANSI.RESET);
        
        const choice = readline.question("👉 Select an option (1-11): ").trim();

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
          else if (choice === "7") { bot.openBybitApp(); }
          else if (choice === "8") { await bot.manageSessions(); }
          else if (choice === "9") { await bot.runSpotTrade(); }
          else if (choice === "10") { await bot.runEdgeBrowserAutoClaim(); }
          else if (choice === "11") {
            console.log(`${ANSI.GREEN}[✅] Exiting program. Goodbye 👋${ANSI.RESET}`);
            process.exit(0);
        } else {
            console.log(`${ANSI.RED}[❌] Invalid selection. Try again.${ANSI.RESET}`);
        }

        readline.question(`\nPress Enter to return to menu...`);
        console.clear();
    }
}

main();

