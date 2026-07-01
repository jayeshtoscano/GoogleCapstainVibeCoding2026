from utils.logger import get_logger

logger = get_logger("observability_agent")

class ObservabilityAgent:

    def __init__(self):

        # In-memory stats (can later move to MongoDB)
        self.metrics = {

            "total_requests": 0,

            "cache_hits": 0,

            "cache_misses": 0,

            "llm_fallbacks": 0,

            "errors": 0,

            "total_latency_ms": 0
        }

    ########################################################
    # MAIN ENTRY
    ########################################################

    def record(self, trace: dict):

        """
        trace contains:
        - cache_hit (bool)
        - fallback_used (bool)
        - latency_ms (float)
        - error (bool)
        """

        logger.info("Recording observability trace")

        self.metrics["total_requests"] += 1

        ####################################################
        # Cache tracking
        ####################################################

        if trace.get("cache_hit"):

            self.metrics["cache_hits"] += 1

        else:

            self.metrics["cache_misses"] += 1

        ####################################################
        # LLM fallback tracking
        ####################################################

        if trace.get("fallback_used"):

            self.metrics["llm_fallbacks"] += 1

        ####################################################
        # Error tracking
        ####################################################

        if trace.get("error"):

            self.metrics["errors"] += 1

        ####################################################
        # Latency tracking
        ####################################################

        latency = trace.get("latency_ms", 0)

        self.metrics["total_latency_ms"] += latency

        ####################################################
        # Compute Diligence Score
        ####################################################

        diligence_score = self._compute_diligence()

        logger.info(
            f"Diligence Score Updated: {diligence_score}"
        )

        return {

            "metrics": self.metrics,

            "diligence": diligence_score,

            "status": self._diligence_status(diligence_score)
        }

    ########################################################
    # DILIGENCE SCORE ENGINE
    ########################################################

    def _compute_diligence(self) -> float:

        total = self.metrics["total_requests"]

        if total == 0:
            return 100.0

        cache_ratio = self.metrics["cache_hits"] / total

        fallback_penalty = (
            self.metrics["llm_fallbacks"] / total
        )

        error_penalty = (
            self.metrics["errors"] / total
        )

        avg_latency = (
            self.metrics["total_latency_ms"] / total
        )

        # Normalize latency (assume 2000ms is bad baseline)
        latency_penalty = min(avg_latency / 2000, 1.0)

        diligence = (

            100
            - (fallback_penalty * 25)
            - (error_penalty * 35)
            - (latency_penalty * 20)
            + (cache_ratio * 20)

        )

        return round(max(min(diligence, 100), 0), 2)

    ########################################################
    # STATUS CLASSIFICATION
    ########################################################

    def _diligence_status(self, score: float) -> str:

        if score >= 85:
            return "EXCELLENT"

        elif score >= 70:
            return "GOOD"

        elif score >= 50:
            return "MODERATE"

        return "POOR"


 def project_scores(self):

        """
        Returns current system health + diligence projection
        """

        diligence = self._compute_diligence()

        return {

            "diligence_score": diligence,

            "status": self._diligence_status(diligence),

            "metrics": self.metrics,

            "breakdown": {

                "cache_hit_ratio":
                    self._safe_div(self.metrics["cache_hits"]),

                "error_rate":
                    self._safe_div(self.metrics["errors"]),

                "fallback_rate":
                    self._safe_div(self.metrics["llm_fallbacks"]),

                "avg_latency_ms":
                    self._avg_latency()

            }
        }
   
    ########################################################
    # HELPERS
    ########################################################

    def _safe_div(self, value):

        total = self.metrics["total_requests"]

        if total == 0:
            return 0.0

        return round(value / total, 4)

    def _avg_latency(self):

        total = self.metrics["total_requests"]

        if total == 0:
            return 0.0

        return round(
            self.metrics["total_latency_ms"] / total,
            2
        )
