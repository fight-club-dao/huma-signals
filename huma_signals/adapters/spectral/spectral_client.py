import datetime

import httpx
import pydantic
import structlog
import asyncio

from huma_signals import models
from huma_signals.settings import settings


logger = structlog.get_logger()


class SpectralScoreIngredients(models.HumaBaseModel):
    credit_mix: int
    defi_actions: int
    health_and_risk: int
    liquidation: int
    market: float
    time: int
    wallet: int


class SpectralWalletSignals(models.HumaBaseModel):
    score: float
    score_ingredients: SpectralScoreIngredients
    score_timestamp: datetime.datetime
    probability_of_liquidation: float
    risk_level: str
    wallet_address: str


class SpectralClient(models.HumaBaseModel):
    """Spectral Client"""

    base_url: str = pydantic.Field(default="https://api.spectral.finance")
    api_key: str = pydantic.Field(
        default=settings.spectral_api_key,
        description="Ethereum private key of the Spectral client",
    )

    @pydantic.validator("base_url")
    def validate_pbase_url(cls, value: str) -> str:
        if not value:
            raise ValueError("spectral base_url is required")
        return value

    @pydantic.validator("api_key")
    def validate_api_key(cls, value: str) -> str:
        if not value:
            raise ValueError("spectral api_key is required")
        return value

    async def _create_score(self, wallet_address: str) -> None:
        try:
            async with httpx.AsyncClient(base_url=self.base_url) as client:
                request = f"/api/v1/addresses/{wallet_address}" f"/calculate_score"
                headers = {"Authorization": f"Bearer {self.api_key}"}
                print(f'{self.base_url}{request}')
                resp = await client.post(request, headers=headers)
                resp.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Error fetching transactions", exc_info=True, request=request)

    async def get_results(self, wallet_address: str):
        try:
            async with httpx.AsyncClient(base_url=self.base_url) as client:
                request = f"/api/v1/addresses/{wallet_address}"
                print(f'{self.base_url}{request}')
                headers = {"Authorization": f"Bearer {self.api_key}"}
                resp = await client.get(request, headers=headers)
                resp.raise_for_status()
                print('response')
                print(resp.json())
                return resp.json()
        except httpx.HTTPStatusError as e:
            logger.error("Error fetching transactions", exc_info=True, request=request)
            raise e

    async def get_scores(self, wallet_address: str) -> SpectralWalletSignals:
        results = await self.get_results(wallet_address)
        if results.get('status') == 'done':
            spectral_signal = SpectralWalletSignals(**results)
            return spectral_signal
        await self._create_score(wallet_address)
        results = await self.get_results(wallet_address)
        while results.get('status') != 'done':
            await asyncio.sleep(10)
            results = await self.get_results(wallet_address)
        return SpectralWalletSignals(**results)

