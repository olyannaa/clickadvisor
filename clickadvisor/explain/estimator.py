from __future__ import annotations

import logging

import httpx

from clickadvisor.explain.parser import EstimateResult, ExplainEstimateParser

logger = logging.getLogger(__name__)


class ExplainEstimator:
    """Запускает EXPLAIN ESTIMATE через HTTP API ClickHouse."""

    def __init__(
        self,
        connect_url: str,
        user: str = "default",
        password: str = "",
    ) -> None:
        self.connect_url = connect_url.rstrip("/")
        self.user = user
        self.password = password
        self.parser = ExplainEstimateParser()

    def estimate(self, sql: str) -> EstimateResult | None:
        """
        Запускает EXPLAIN ESTIMATE для SQL.
        Возвращает агрегированный EstimateResult или None при ошибке.
        """
        explain_sql = f"EXPLAIN ESTIMATE {sql}"

        try:
            response = httpx.get(
                f"{self.connect_url}/",
                params={
                    "query": explain_sql,
                    "user": self.user,
                    "password": self.password,
                },
                timeout=30.0,
            )
            response.raise_for_status()

            results = self.parser.parse(response.text)
            if not results:
                return None
            return self.parser.aggregate(results)
        except Exception as error:
            logger.warning("EXPLAIN ESTIMATE failed: %s", error)
            return None
