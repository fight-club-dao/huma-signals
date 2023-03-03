# Spectral Wallet Signal Adapter

This is the repository for the Signal Adapter to fetch credit scores and default probabilities for a wallet address.
Keep in mind that only arbitrum, polygon, goleri, and mainnet wallets are supported.

## Type of signals

- score: The credit score of the wallet address
- score_ingredients: object containing the ingredients of the score
  - credit_mix: Consideration of the number of DeFi lending protocols interacted with to assess the protocol concentration risk.
  - defi_actions: Assessment of the various transactions undertaken on the DeFi lending protocols, e.g. borrowing, repayments, deposits, etc.
  - health_and_risk: Evaluation of the amount of headroom maintained as part of your borrowing activities, similar to LTV.
  - liquidation: Consideration of any historical liquidation events triggered on any of the bundled wallets.
  - market: Evaluation of the general market volatility at the time of one's on-chain activities.
  - time: Analysis of various time-based factors, e.g. length of wallet history.
  - wallet: Assessment of the trend of wallet balance, transactions, and its composition.
- score_timestamp: time when the score was created
- probability_of_liquidation: the chance of the wallet address to be liquidated
- risk_level: Describes the level of risk associated with the wallet. Possible values are: VERY_HIGH_RISK, HIGH_RISK, MEDIUM_RISK, LOW_RISK, VERY_LOW_RISK
- wallet_address: Ethereum wallet address

## Local Development

See [here](../../../docs/getting_started.md) for the development guide.

## Required environment variable

The following environment variable is required to run the adapter.
(Sign up at https://polygonscan.com/myapikey to get an API key)

```bash
SPECTRAL_API_KEY
```

## Tests

```bash
make test
```
