# 10 秒折扣大挑戰！——STM32 智慧計時折扣挑戰機

**10-Second Discount Challenge | STM32 Smart Discount Timer**

## 1. 故事背景與設計動機

### 1.1 故事背景

假設今天我們經營一家商店，為了吸引更多顧客，希望推出一項與一般促銷活動不同的優惠方案。

傳統的折扣活動通常由店家直接提供固定優惠，顧客只需要消費就能享有折扣，缺乏互動性。

因此，我們決定設計一款「10 秒折扣大挑戰」，讓顧客透過自己的時間感來決定能獲得多少優惠。

### 1.2 活動規則

顧客只需要按下按鈕開始計時，再憑自己的感覺，在接近 10 秒時按下按鈕停止計時。

系統會自動計算實際時間與 10 秒的誤差，並決定折扣：

| 時間誤差 | 獲得折扣 |
|---|---|
| ≤ 0.05 秒 | 5 折 |
| ≤ 0.20 秒 | 7 折 |
| ≤ 1.00 秒 | 9 折 |
| > 1.00 秒 | 10 折（原價） |

當顧客成功獲得優惠時，LED 會產生呼吸燈效果閃三下，增加活動的趣味性。

### 1.3 專題目標

本專題希望透過 STM32 微控制器，將傳統折扣活動轉換成具有互動性的遊戲。

系統整合按鈕控制、硬體計時、折扣計算、UART 通訊、Python GUI 顯示及 PWM LED 燈效，讓店家能以簡單的設備舉辦互動促銷活動。

### 1.4 系統介紹

本系統使用 STM32 NUCLEO-G474RE 開發板作為核心控制器。

玩家透過 B1 按鈕操作遊戲，STM32 負責計時及計算折扣，並透過 UART 將結果傳送到電腦上的 Python GUI。

當玩家獲得折扣時，系統會透過 TIM3 PWM 控制 LED，產生三次漸亮、漸暗的呼吸燈效果。

## 2. 開發環境（Development Environment）

### 2.1 硬體設備

- STM32 NUCLEO-G474RE 開發板
- USB 傳輸線
- 麵包板
- 黃色 LED
- 限流電阻
- 杜邦線
- 電腦

### 2.2 軟體工具

- STM32CubeIDE
- STM32 HAL Library
- Python 3
- tkinter（GUI 圖形化介面）
- pyserial（UART 串列通訊）
- GitHub（程式碼版本管理）

### 2.3 通訊設定

| 項目 | 設定 |
|---|---|
| UART | LPUART1 |
| Baud Rate | 115200 |
| Data Bits | 8 |
| Parity | None |
| Stop Bits | 1 |
| 傳輸方式 | ST-LINK Virtual COM Port |

## 3. 系統架構（System Architecture）

本專題主要由 STM32 微控制器、按鈕輸入、計時器、UART 通訊、Python GUI 與 PWM LED 組成。

### 3.1 系統運作流程

1. 系統初始化 GPIO、TIM2、TIM3 與 LPUART1。
2. 玩家第一次按下 B1 按鈕，STM32 開始計時。
3. 玩家第二次按下 B1 按鈕，STM32 停止計時。
4. 系統計算經過時間及與 10 秒的誤差。
5. 根據誤差決定折扣。
6. 透過 UART 傳送結果至電腦。
7. Python GUI 顯示計時、誤差及折扣。
8. 若玩家獲得折扣，LED 執行三次呼吸燈效果。
9. 系統回到等待下一次挑戰的狀態。

### 3.2 STM32 腳位配置

| 腳位 | 功能 | 說明 |
|---|---|---|
| PC13 | GPIO EXTI | B1 按鈕輸入 |
| PA2 | LPUART1 TX | 傳送資料至電腦 |
| PA3 | LPUART1 RX | 接收 UART 資料 |
| PA6 | TIM3 CH1 PWM | 控制外接 LED |
| GND | Ground | LED 電路接地 |

## 4. 系統功能說明（System Features）

### 4.1 按鈕控制

使用 STM32 開發板上的 B1 按鈕（PC13）進行遊戲控制。

- 第一次按下：開始計時。
- 第二次按下：停止計時。
- 計算完成後：準備下一次挑戰。

按鈕使用 GPIO 外部中斷（EXTI）偵測，不需要持續輪詢按鈕狀態。

### 4.2 計時功能

使用 TIM2 計時器計算玩家的實際經過時間。

目標時間固定為 **10 秒**。

系統停止計時後，計算實際時間與目標時間的絕對誤差：

**時間誤差 = |實際時間 − 10 秒|**

### 4.3 折扣計算

系統根據時間誤差決定折扣：

| 時間誤差 | 折扣 |
|---|---|
| ≤ 0.05 秒 | 5 折 |
| ≤ 0.20 秒 | 7 折 |
| ≤ 1.00 秒 | 9 折 |
| > 1.00 秒 | 10 折（無折扣） |

玩家越接近 10 秒，獲得的折扣越高。

### 4.4 UART 通訊與 Python GUI

STM32 使用 LPUART1 與電腦進行 UART 通訊。

當玩家完成計時後，STM32 將以下資訊傳送至電腦：

- Time：實際計時結果
- Error：時間誤差
- Discount：折扣結果

電腦端使用 Python tkinter 建立圖形化介面，並透過 pyserial 接收 STM32 傳送的資料。

GUI 可顯示遊戲結果與 UART 接收紀錄，方便使用者觀察系統運作。

### 4.5 PWM LED 呼吸燈

本專題使用 TIM3 Channel 1 輸出 PWM 訊號，透過 PA6 控制外接黃色 LED。

當玩家獲得折扣時，系統改變 PWM Duty Cycle，使 LED 亮度逐漸增加再逐漸降低，形成呼吸燈效果。

- 獲得 5 折、7 折或 9 折：LED 呼吸三次。
- 10 折（無折扣）：LED 維持熄滅。

## 5. 核心技術（Core Technologies）

### 5.1 GPIO 與外部中斷（EXTI）

使用 PC13 偵測 B1 按鈕的按下事件，透過 GPIO 外部中斷觸發 Callback。

使用的 HAL 函式包含：

- `HAL_GPIO_EXTI_Callback()`
- `HAL_GPIO_Init()`

### 5.2 TIM2 硬體計時器

TIM2 負責記錄開始與停止計時的時間點。

透過硬體計時器計算經過時間，避免單純依賴軟體延遲進行計時。

主要使用：

- `HAL_TIM_Base_Start()`
- `__HAL_TIM_GET_COUNTER()`

### 5.3 UART 串列通訊

使用 LPUART1 將計時結果傳送至電腦。

主要使用：

- `HAL_UART_Transmit()`
- `HAL_UART_Receive_IT()`

電腦端透過 Python pyserial 接收並處理資料。

### 5.4 TIM3 PWM 控制

使用 TIM3 Channel 1 產生 PWM 訊號，控制 LED 的亮度變化。

主要使用：

- `HAL_TIM_PWM_Start()`
- `__HAL_TIM_SET_COMPARE()`

透過調整比較值改變 Duty Cycle，實現 LED 漸亮與漸暗。

### 5.5 狀態控制

系統透過 `game_state` 變數管理遊戲流程。

| 狀態 | 功能 |
|---|---|
| 0 | 等待開始 |
| 1 | 正在計時 |
| 2 | 停止計時並處理結果 |

透過狀態控制避免按鈕操作與結果處理互相干擾。

## 6. 硬體接線（Hardware Connections）

### 6.1 B1 按鈕

使用 NUCLEO-G474RE 開發板內建 B1 按鈕。

- 腳位：PC13
- 模式：GPIO External Interrupt

不需要額外接線。

### 6.2 UART 通訊

使用開發板的 ST-LINK Virtual COM Port 與電腦通訊。

- PA2：LPUART1 TX
- PA3：LPUART1 RX
- Baud Rate：115200

### 6.3 LED 接線

外接黃色 LED 使用 PA6 的 TIM3 CH1 PWM 訊號控制。

接線方式：

**PA6 → 限流電阻 → LED 正極（Anode）→ LED 負極（Cathode）→ GND**

透過 PWM 訊號控制 LED 亮度。

## 7. 軟體設計（Software Design）

### 7.1 STM32 程式

STM32 端主要負責：

- 初始化 GPIO、TIM2、TIM3、UART。
- 處理 B1 按鈕外部中斷。
- 記錄計時器數值。
- 計算時間誤差。
- 判斷折扣。
- 透過 UART 傳送結果。
- 控制 PWM LED 呼吸燈。

主要程式位於：

`Core/Src/main.c`

### 7.2 Python GUI 程式

電腦端使用 Python tkinter 建立圖形化介面。

主要功能：

- 選擇 UART COM Port。
- 建立或中斷串列連線。
- 接收 STM32 傳送的資料。
- 顯示 Time、Error、Discount。
- 顯示 UART 接收紀錄。

Python 程式檔案：

`UART_test.py`

## 8. 操作方式（How to Use）

### 8.1 啟動系統

1. 使用 USB 將 STM32 NUCLEO-G474RE 連接至電腦。
2. 確認 STM32 已燒錄專題程式。
3. 在電腦執行 `UART_test.py`。
4. 選擇 STM32 對應的 COM Port。
5. 設定 Baud Rate 為 115200。
6. 按下 Connect 建立 UART 連線。

### 8.2 開始遊戲

1. 第一次按下 B1 按鈕，開始計時。
2. 玩家自行判斷接近 10 秒的時機。
3. 第二次按下 B1 按鈕，停止計時。
4. 系統自動計算時間誤差與折扣。
5. Python GUI 顯示遊戲結果。
6. 若獲得折扣，LED 執行三次呼吸燈效果。

## 9. 測試結果（Testing Results）

目前已完成以下功能測試：

| 測試項目 | 結果 |
|---|---|
| B1 按鈕開始計時 | 通過 |
| B1 按鈕停止計時 | 通過 |
| TIM2 計時功能 | 通過 |
| 10 秒目標時間 | 通過 |
| 時間誤差計算 | 通過 |
| 折扣結果判斷 | 通過 |
| UART 傳送結果 | 通過 |
| Python GUI 顯示結果 | 通過 |
| TIM3 PWM 控制 LED | 通過 |
| LED 呼吸燈效果 | 通過 |

### 9.1 測試說明

經實際測試，系統可以正常執行按鈕計時、誤差計算、折扣判斷、UART 資料傳送與 Python GUI 顯示。

外接 LED 也可以根據折扣結果執行 PWM 呼吸燈效果。

### 9.2 成果展示

此處可加入：

- STM32 開發板與麵包板接線照片。
- Python GUI 執行畫面。
- 不同折扣結果的測試截圖。
- LED 呼吸燈展示影片。

## 10. 專題總結（Conclusion）

本專題整合 STM32 微控制器的 GPIO 外部中斷、硬體計時器、UART 串列通訊及 PWM 控制，完成一套具有互動功能的智慧計時折扣挑戰機。

透過 B1 按鈕控制遊戲流程，使用 TIM2 進行計時，根據時間誤差計算折扣，再利用 UART 將結果傳送至 Python GUI 顯示，並使用 TIM3 PWM 控制 LED 呼吸燈。

透過本次專題，實際練習 STM32CubeIDE 開發環境、HAL 函式庫、硬體周邊設定、中斷處理、計時器操作、UART 通訊與 PWM 控制，並將嵌入式系統與電腦端圖形化介面整合。

本系統目前已完成主要功能並通過實際操作測試。
