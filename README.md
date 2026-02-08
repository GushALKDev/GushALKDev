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

### 📈 Synthetic Trading Protocol (In progress...)

_A high-leverage synthetic futures platform utilizing a Single-Sided Liquidity (SSL) Unified Vault and a 3-layer solvent defense system._ [**View Repository**](https://github.com/GushALKDev/evm-synthetic-trading-protocol)

- **Single-Sided Liquidity (SSL):** Unified USDC Vault acting as the global counterparty (PvPool model: Traders vs LPs), eliminating liquidity fragmentation across trading pairs.
- **Hybrid Solvency Engine:** A 3-layer defense system featuring **Preventive** (Adaptive OI based on Volatility), **Reactive** (Assistant Fund injection), and ($SYNTH Bonding) mechanisms.
- **Oracle Aggregation (DON):** Custom Decentralized Oracle Network aggregating prices from 6-8 nodes (median filtering) with Chainlink validation to prevent price manipulation.
- **Oracle-Based Execution:** Enables large size trades at oracle price, utilizing dynamic spreads (based on OI and Volatility) to simulate market depth and protect LPs.
- **Tech:** Solidity, Foundry, ERC-4626, Chainlink Oracles, Custom DON (Decentralized Oracle Network), Solady.

### 🛡️ Yield Bearing Vaults Protocol

_A modular ERC-4626 production-grade architecture decoupling vault accounting from yield strategies._ [**View Repository**](https://github.com/GushALKDev/evm-yield-bearing-vaults)

- **Modular Architecture:** Decoupled Vault/Strategy pattern enabling atomic pass-through deposits; funds route instantly (User → Vault → Strategy → Protocol) in a single transaction.
- **Leveraged Loop:** Engineered an atomic **Uniswap V4 Flash Loan** (zero fee) & **Aave V3 E-Mode** strategy to cycle liquidity, maximizing LTV (up to 93%) and capturing yield spread with up to 10x leverage. Proportional deleverage maintains leverage ratio on withdrawals.
- **Automatic Health Monitoring:** Continuous position health checks with automatic emergency divest when health factor drops below threshold, preventing liquidations while maintaining user fund access.
- **Emergency Recovery:** Seamless automatic reinvestment when emergency mode is deactivated, restoring leveraged positions without manual intervention.
- **Defensive Security:** Implemented critical protections including **Emergency Circuit Breakers**, **Reentrancy Guards**, **Inflation Attack Prevention** (Dead Shares), **Optimized Withdrawals** (skip divest during emergency), and access-controlled emergency activation.
- **Financial Integrity:** Enforced **High Water Mark** accounting to align fees with net performance.
- **Gas Optimizations:** Storage packing (~40k gas deployment savings), computation caching (~250-400 gas per flash loan), batch whitelist operations (~21k gas per additional address), and unchecked math where safe.
- **Testing & Coverage:** **205 tests** achieving **93.72% coverage** with **352,608+ total iterations**. Includes **27 stateful fuzzing invariant tests** using the handler pattern (BaseVaultHandler, WETHLoopStrategyHandler, AdminHandler) with ghost variable tracking. Supports **dual-mode execution**: mock mode (345,600 operations, 256 runs × 50 depth) for fast iteration, and fork mode (real Aave V3 + Uniswap V4) for protocol validation.
- **Tech:** Solidity 0.8.26, Foundry, ERC-4626, Aave V3, Uniswap V4, OpenZeppelin.

### 🔮 Prediction Market Protocol (Private R&D)

_An advanced decentralized prediction market architected from scratch focusing on capital efficiency and atomic execution._

- **Virtual CPMM Math:** Engineered a custom **Virtual Liquidity AMM** to prevent liquidity draining and ensure continuous price discovery (soft bounds).
- **Mechanism Design:** Implements an **"Entry Toll" fee model** (High Entry / Zero Exit) to maximize revenue while incentivizing arbitrage rebalancing.
- **Architecture:** Decoupled trading logic from custody (Gnosis CTF), implementing an **Atomic Router** for 1-click swaps and quadratic exit calculations.
- **Security & Ops:** Features **Inflation Attack Protection** (dead shares), **CREATE2** deterministic deployment, and rigorous invariant testing.
- **Tech:** Solidity, Foundry, Gnosis Conditional Tokens, OpenZeppelin.

### 🏛️ Multi-Level Real Yield Staking (O(1) Algorithm)

_A hardened staking contract designed to solve linear gas scaling issues in reward distribution._ [**View Repository**](https://github.com/GushALKDev/evm-dexynth-multilevel-real-yield-staking)

- **The Breakthrough:** Replaced legacy loop-based reward logic with an **"O(1) accumulator model"**.
- **Impact:** Achieved **~97% gas reduction** for claiming rewards, ensuring constant-time execution regardless of staker count.
- **Features:** Lock-up levels, Real Yield distribution, and emergency withdraw mechanics.

### 🌌 Pulsar DAO (Solana/Rust)

_Redefining governance on Solana to combat voter apathy and whale dominance._ [**View Repository**](https://github.com/GushALKDev/solana_pulsar_dao)

- **Architecture:** Implements a novel **Hybrid Voting model** with Proxy Lock security and Trustless Treasury execution.
- **Stack:** Built purely in **Rust** using the **Anchor** framework.

### 🤖 GMX V2 AI Agent

_Bridging the gap between Natural Language Processing (NLP) and DeFi execution._ [**View Repository**](https://github.com/GushALKDev/gmx-v2-ai-agent)

- **Functionality:** An AI-powered conversational bot capable of executing complex trades on **GMX V2 (Arbitrum)** via Telegram commands.
- **Tech:** Node.js, TypeScript, OpenAI API, Ethers.js.

---

## 🛡️ Security Research & Auditing

My development philosophy is "Audit-Ready by Default." I actively conduct security reviews and practice advanced testing methodologies.

| Protocol Type       | Focus Area                                 | Tools Used             |
| :------------------ | :----------------------------------------- | :--------------------- |
| **Vault Guardians** | ERC-4626 Compliance & Access Control       | Foundry, Fuzzing       |
| **Thunder Loan**    | Flash Loans & Oracle Manipulation          | Manual Review, Slither |
| **Boss Bridge**     | L1<->L2 Message Passing & Signature Replay | Stateless Fuzzing      |
| **TSwap AMM**       | Invariant Analysis (k=x\*y)                | Invariant Testing      |

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
