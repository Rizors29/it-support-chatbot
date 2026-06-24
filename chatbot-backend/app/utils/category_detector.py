def detect_category(query: str, sources: list[str] | None = None) -> str:
    text = query.lower()

    if sources:
        text += " " + " ".join(sources).lower()

    # Prioritas spesifik dulu
    if any(keyword in text for keyword in ["printer", "c3371", "fuji", "xerox", "print"]):
        return "Printer"

    if any(keyword in text for keyword in ["mfa", "authenticator", "registrasi microsoft", "otp", "kode verifikasi", "microsoft 365"]):
        return "Microsoft 365"

    if any(keyword in text for keyword in ["drive tidak muncul", "ssd", "harddisk", "storage", "penyimpanan", "m.2"]):
        return "Windows"

    if any(keyword in text for keyword in ["windows", "install windows", "boot", "bios"]):
        return "Windows"

    if any(keyword in text for keyword in ["wifi", "network", "internet", "ethernet", "vpn"]):
        return "Network"

    return "General"