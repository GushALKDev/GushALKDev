# Hi there, I'm Gustavo Martín 👋

### Senior Smart Contract Engineer | Security Researcher | DeFi Architecture

[![Linkedin](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/gustavomaral/)

> **"Critical systems cannot fail."**
> From engineering SCADA controls for particle accelerators at **CERN** to architecting **complex DeFi protocols**. I specialize in building **zero-to-one financial infrastructure**, gas-optimized state machines (O(1)), and securing smart contracts through invariant testing and formal verification.

---

## 🛠️ Tech Stack & Tools

![Solidity](https://img.shields.io/badge/Solidity-%23363636.svg?style=for-the-badge&logo=solidity&logoColor=white)
![Foundry](https://img.shields.io/badge/Foundry-%23N/A.svg?style=for-the-badge&logo=foundry&logoColor=white)
![Rust/Anchor](https://img.shields.io/badge/Rust_/_Anchor-%23000000.svg?style=for-the-badge&logo=rust&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![NestJS](https://img.shields.io/badge/nestjs-%23E0234E.svg?style=for-the-badge&logo=nestjs&logoColor=white)
![Go](https://img.shields.io/badge/go-%2300ADD8.svg?style=for-the-badge&logo=go&logoColor=white)

---

## 🚀 Featured Engineering & Architecture

### 🛡️ Yield Bearing Vaults Protocol (Beta)
*A modular ERC-4626 production-grade architecture decoupling vault accounting from yield strategies.* [**View Repository**](https://github.com/GushALKDev/evm-yield-bearing-vaults)
- **Modular Architecture:** Separates **Vault** (Accounting, User Interface) from **Strategy** (Yield Logic), allowing interchangeable strategies (e.g., Aave).
- **Security First:** Includes **Inflation Attack Protection** (Dead Shares), **Circuit Breaker** (Emergency Pause), and strict **Access Control**.
- **Performance Fees:** Implements a **High Water Mark** mechanism to charge fees only on net profits.
- **Status:** **Work In Progress (Beta)**. Core functionality tested. Unaudited.
- **Tech:** Solidity 0.8.33, Foundry, ERC-4626, Aave V3, OpenZeppelin.

### 🔮 Prediction Market Protocol (Private R&D)
*An advanced decentralized prediction market architected from scratch focusing on capital efficiency and atomic execution.*
- **Core Architecture:** Implements a custom **CPMM (Constant Product Market Maker)** specifically tuned for binary outcome trading.
- **Innovation:** Features **Virtual Liquidity** mechanics and 1-click atomic trading (Collateral ↔ Position) to reduce UX friction.
- **Security:** Includes a dual-fee structure and advanced quadratic exit math, rigorously secured via **Foundry invariant tests**.
- **Tech:** Solidity, Foundry, Gnosis Conditional Tokens, OpenZeppelin.

### 🏛️ Multi-Level Real Yield Staking (O(1) Algorithm)
*A hardened staking contract designed to solve linear gas scaling issues in reward distribution.* [**View Repository**](https://github.com/GushALKDev/evm-dexynth-multilevel-real-yield-staking)
- **The Breakthrough:** Replaced legacy loop-based reward logic with an **"O(1) accumulator model"**.
- **Impact:** Achieved **~97% gas reduction** for claiming rewards, ensuring constant-time execution regardless of staker count.
- **Features:** Lock-up levels, Real Yield distribution, and emergency withdraw mechanics.

### 🌌 Pulsar DAO (Solana/Rust)
*Redefining governance on Solana to combat voter apathy and whale dominance.* [**View Repository**](https://github.com/GushALKDev/solana_pulsar_dao)
- **Architecture:** Implements a novel **Hybrid Voting model** with Proxy Lock security and Trustless Treasury execution.
- **Stack:** Built purely in **Rust** using the **Anchor** framework.

### 🤖 GMX V2 AI Agent
*Bridging the gap between Natural Language Processing (NLP) and DeFi execution.* [**View Repository**](https://github.com/GushALKDev/gmx-v2-ai-agent)
- **Functionality:** An AI-powered conversational bot capable of executing complex trades on **GMX V2 (Arbitrum)** via Telegram commands.
- **Tech:** Node.js, TypeScript, OpenAI API, Ethers.js.

---

## 🛡️ Security Research & Auditing

My development philosophy is "Audit-Ready by Default." I actively conduct security reviews and practice advanced testing methodologies.

| Protocol Type | Focus Area | Tools Used |
| :--- | :--- | :--- |
| **Vault Guardians** | ERC-4626 Compliance & Access Control | Foundry, Fuzzing |
| **Thunder Loan** | Flash Loans & Oracle Manipulation | Manual Review, Slither |
| **Boss Bridge** | L1<->L2 Message Passing & Signature Replay | Stateless Fuzzing |
| **TSwap AMM** | Invariant Analysis (k=x*y) | Invariant Testing |

---

## 🏗️ Backend & Infrastructure

Beyond smart contracts, I architect the off-chain nervous system that powers DeFi protocols.

- **[EIP-712 Verification](https://github.com/GushALKDev/evm-eip-712-wallet-verification):** Secure off-chain signature verification system for gasless interactions.
- **[NestJS Teslo Shop](https://github.com/GushALKDev/nestjs-teslo-shop):** Full-scale e-commerce backend demonstrating robust architectural patterns (Modules, Guards, Interceptors).
- **[Go Events API](https://github.com/GushALKDev/go-events-rest-api):** High-performance REST API built with Go and Gin.

---

### 💻 Tech Stack Distribution
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=GushALKDev&layout=compact&theme=radical&hide_border=true&bg_color=0d1117&title_color=58a6ff&icon_color=58a6ff&hide=html,css" height="200" alt="languages graph" />

---

<div align="center">
  <sub><em>"Talk is cheap. Show me the code." — Linus Torvalds</em></sub>
</div>