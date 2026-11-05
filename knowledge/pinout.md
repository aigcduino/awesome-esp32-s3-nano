---
title: WT9932S3-NANO 引脚定义与 GPIO 对照
board: Wireless-TAG WT9932S3-NANO
source: https://wiki.wireless-tag.com/docs/zh/WT9932S3-NANO/board_features.html
retrieved: 2026-11-05
tags: [wt9932s3-nano, 引脚, pinout, gpio, i2c, spi, uart]
---

# WT9932S3-NANO 引脚定义

`D0–D13` / `A0–A7` 是 **Arduino 引脚编号**，与芯片 GPIO 编号不是一回事。写代码或抄示例时必须按这张表换算。

## 左排针

| 序号 | 引脚 | 功能 | 电平 | ESP-IDF GPIO |
|---|---|---|---|---|
| 1 | D13 | GPIO / SPI SCK | 0V/3.3V | GPIO48 |
| 2 | 3.3V | 3.3V 电源输出 | 3.3V | — |
| 3 | B0 | GPIO | 0V/3.3V | GPIO46 |
| 4 | A0 | GPIO | 0V/3.3V | GPIO1 |
| 5 | A1 | GPIO | 0V/3.3V | GPIO2 |
| 6 | A2 | GPIO | 0V/3.3V | GPIO3 |
| 7 | A3 | GPIO | 0V/3.3V | GPIO4 |
| 8 | A4 | GPIO / I2C SDA | 0V/3.3V | GPIO11 |
| 9 | A5 | GPIO / I2C SCL | 0V/3.3V | GPIO12 |
| 10 | A6 | GPIO | 0V/3.3V | GPIO13 |
| 11 | A7 | GPIO | 0V/3.3V | GPIO14 |
| 12 | VBUS | VBUS 电源 | 5V | — |
| 13 | B1 | GPIO | 0V/3.3V | GPIO0（BOOT） |
| 14 | GND | 地 | 0V | — |
| 15 | VIN | 外部电源输入 | 5V | — |

## 右排针

| 序号 | 引脚 | 功能 | 电平 | ESP-IDF GPIO |
|---|---|---|---|---|
| 1 | D12 | GPIO / SPI MISO | 0V/3.3V | GPIO47 |
| 2 | D11 | GPIO / SPI MOSI | 0V/3.3V | GPIO38 |
| 3 | D10 | GPIO | 0V/3.3V | GPIO21 |
| 4 | D9 | GPIO | 0V/3.3V | GPIO18 |
| 5 | D8 | GPIO | 0V/3.3V | GPIO17 |
| 6 | D7 | GPIO | 0V/3.3V | GPIO10 |
| 7 | D6 | GPIO | 0V/3.3V | GPIO9 |
| 8 | D5 | GPIO | 0V/3.3V | GPIO8 |
| 9 | D4 | GPIO | 0V/3.3V | GPIO7 |
| 10 | D3 | GPIO | 0V/3.3V | GPIO6 |
| 11 | D2 | GPIO | 0V/3.3V | GPIO5 |
| 12 | GND | 地 | 0V | — |
| 13 | RST | 复位引脚 | 0V/3.3V | EN |
| 14 | D0 | GPIO / RXD | 0V/3.3V | GPIO44 |
| 15 | D1 | GPIO / TXD | 0V/3.3V | GPIO43 |

## 常用总线速查

- I2C：SDA = A4 = GPIO11，SCL = A5 = GPIO12
- SPI：SCK = D13 = GPIO48，MISO = D12 = GPIO47，MOSI = D11 = GPIO38
- UART0（日志/烧录）：TXD = D1 = GPIO43，RXD = D0 = GPIO44，115200 8N1
- BOOT：B1 = GPIO0
