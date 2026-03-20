THREAT_RULES = {
    "trojan": {
        "title": "Malware Blocked",
        "why": "The file contains malicious or unsafe code.",
        "explanation": "Windows Defender detected harmful behavior and blocked the file before it could run.",
        "steps": [
            "Do not open the file.",
            "Delete the file if you do not trust it.",
            "Run a full system scan."
        ],
        "severity": "Critical"
    },
    "pua": {
        "title": "Potentially Unwanted App Blocked",
        "why": "This application may change settings, show ads, or affect performance.",
        "explanation": "The app may not be strict malware, but it can still negatively affect your PC.",
        "steps": [
            "Review where the file came from.",
            "Remove it if you do not need it.",
            "Run a scan if you are unsure."
        ],
        "severity": "Warning"
    },
    "eicar": {
        "title": "Security Test Success",
        "why": "The EICAR test file was detected.",
        "explanation": "This is a harmless antivirus test file used to verify that protection is working.",
        "steps": [
            "No action is required.",
            "Your Defender detection pipeline is working."
        ],
        "severity": "Informational"
    }
}