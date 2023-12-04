from datetime import datetime, timezone


def inject_utcnow(request):
    return {"utcnow": datetime.now(timezone.utc)}
