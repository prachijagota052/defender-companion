# packages/logic/rules.py

THREAT_RULES = {
    "trojan": {
        "title": "Malware Blocked",
        "why": "The file contains malicious code.",
        "explanation": "Windows detected harmful behavior and stopped the file before it could run.",
        "steps": [
            "Do not open the file.",
            "Delete it if not needed.",
            "Run a full system scan."
        ],
        "severity": "Critical"
    },
    "pua": {
        "title": "Potentially Unwanted App Blocked",
        "why": "This application may affect system performance or show ads.",
        "explanation": "The app is not strictly harmful but may change settings or install unwanted components.",
        "steps": [
            "Review the file source.",
            "Remove it if unnecessary."
        ],
        "severity": "Warning"
    },
    "eicar": {
        "title": "Security Test Success",
        "why": "The EICAR test file was detected.",
        "explanation": "This is a harmless file used to verify that your protection is active.",
        "steps": ["No action needed.", "Your system is working perfectly!"],
        "severity": "Info"
    }
}
