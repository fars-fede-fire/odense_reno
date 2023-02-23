"""API wrapper of Odense Renovation."""

from __future__ import annotations

import asyncio
from datetime import date, timedelta
from typing import Any
from dataclasses import dataclass

from aiohttp.client import ClientSession
import async_timeout


@dataclass
class OdenseReno:
    """Main class for handling data from Odense Renovation."""

    address_no: int
    session: ClientSession | None = None
    request_timeout: int = 10
    _close_session: bool = False

    async def _request(self, url: str) -> dict[str, Any]:
        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request("GET", url)
        except asyncio.TimeoutError as exception:
            raise OdenseRenoConnectionError(
                "Timeout while trying to connect to Odense Reno API."
            ) from exception

        return await response.json()

    async def _update(self) -> dict[str, Any]:
        """Fetch dates and wastetypes from Odense Reno"""
        start_date = date.today()
        end_date = date.today() + timedelta(days=365)

        url = f"https://mit.odenserenovation.dk/api/Calendar/GetCalendarByAddress?addressNo={self.address_no}&startDate={start_date}&endDate={end_date}"

        return await self._request(url)

    async def get_adress(self) -> str:
        """Get address of address_no"""
        response = await self._update()
        adress = response["Address"]["PrettyAddress"]

        return adress

    async def get_pickup_dates(self) -> dict[str, list[date]]:
        """Get pickup dates for waste types."""

        response = await self._update()

        waste_types = [item["Label"] for item in response["AvailableBins"]]

        pickups = {waste_type: [] for waste_type in waste_types}

        for pickup in response["Months"]:
            for bin in pickup["Days"]:
                pickup_date = bin["Date"]
                pickup_type = bin["Bins"]
                for i in pickup_type:
                    typetype = i["Label"]
                    pickups[typetype].append(pickup_date)

        for waste_type in pickups:
            pickups[waste_type].sort()

        return pickups

    async def close(self) -> None:
        """Close client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> OdenseReno:
        """Async enter."""
        return self

    async def __aexit__(self, *_exc_info: Any) -> None:
        """Async exit."""

        await self.close()


class OdenseRenoError(Exception):
    """Generic Odense Reno exception."""


class OdenseRenoConnectionError(OdenseRenoError):
    """Odense Reno connection exception."""
