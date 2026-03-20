import os


TITLE_MAP = {
    "en": {
        "Malware Blocked": "Malware Blocked",
        "Potentially Unwanted App Blocked": "Potentially Unwanted App Blocked",
        "Security Test Success": "Security Test Success",
        "Threat Detected": "Threat Detected",
        "Windows Defender Setting Changed": "Windows Defender Setting Changed",
    },
    "hi": {
        "Malware Blocked": "मैलवेयर रोका गया",
        "Potentially Unwanted App Blocked": "संभावित रूप से अवांछित ऐप रोका गया",
        "Security Test Success": "सुरक्षा परीक्षण सफल",
        "Threat Detected": "खतरा पाया गया",
        "Windows Defender Setting Changed": "विंडोज डिफेंडर सेटिंग बदली गई",
    },
    "mr": {
        "Malware Blocked": "मालवेअर रोखले गेले",
        "Potentially Unwanted App Blocked": "संभाव्य अवांछित अॅप रोखले गेले",
        "Security Test Success": "सुरक्षा चाचणी यशस्वी",
        "Threat Detected": "धोका आढळला",
        "Windows Defender Setting Changed": "विंडोज डिफेंडर सेटिंग बदलली गेली",
    },
}

EXPLANATION_MAP = {
    "en": {
        "This file contains a signature used for security testing. It has been isolated to keep your system safe.":
            "This file contains a signature used for security testing. It has been isolated to keep your system safe.",
        "Windows Defender detected harmful behavior and blocked the file before it could run.":
            "Windows Defender detected harmful behavior and blocked the file before it could run.",
        "The app may not be strict malware, but it can still negatively affect your PC.":
            "The app may not be strict malware, but it can still negatively affect your PC.",
        "Windows Defender identified this item and blocked or logged it to help protect your PC.":
            "Windows Defender identified this item and blocked or logged it to help protect your PC.",
        "This does not always mean malware, but security-related settings were modified and should be reviewed.":
            "This does not always mean malware, but security-related settings were modified and should be reviewed.",
    },
    "hi": {
        "This file contains a signature used for security testing. It has been isolated to keep your system safe.":
            "इस फ़ाइल में सुरक्षा परीक्षण के लिए उपयोग की जाने वाली सिग्नेचर है। आपके सिस्टम को सुरक्षित रखने के लिए इसे अलग कर दिया गया है।",
        "Windows Defender detected harmful behavior and blocked the file before it could run.":
            "विंडोज डिफेंडर ने हानिकारक व्यवहार का पता लगाया और फ़ाइल को चलने से पहले रोक दिया।",
        "The app may not be strict malware, but it can still negatively affect your PC.":
            "यह ऐप सीधे तौर पर मैलवेयर नहीं हो सकता, लेकिन यह आपके पीसी को प्रभावित कर सकता है।",
        "Windows Defender identified this item and blocked or logged it to help protect your PC.":
            "विंडोज डिफेंडर ने इस आइटम की पहचान की और आपके पीसी की सुरक्षा के लिए इसे ब्लॉक या लॉग किया।",
        "This does not always mean malware, but security-related settings were modified and should be reviewed.":
            "इसका मतलब हमेशा मैलवेयर नहीं होता, लेकिन सुरक्षा से जुड़ी सेटिंग बदली गई है और उसकी जाँच करनी चाहिए।",
    },
    "mr": {
        "This file contains a signature used for security testing. It has been isolated to keep your system safe.":
            "या फाइलमध्ये सुरक्षा चाचणीसाठी वापरली जाणारी सिग्नेचर आहे. तुमची प्रणाली सुरक्षित ठेवण्यासाठी ती वेगळी ठेवली आहे.",
        "Windows Defender detected harmful behavior and blocked the file before it could run.":
            "विंडोज डिफेंडरने हानिकारक वर्तन ओळखले आणि फाइल चालू होण्यापूर्वीच रोखली.",
        "The app may not be strict malware, but it can still negatively affect your PC.":
            "हे अॅप थेट मालवेअर नसले तरी तुमच्या पीसीवर वाईट परिणाम करू शकते.",
        "Windows Defender identified this item and blocked or logged it to help protect your PC.":
            "विंडोज डिफेंडरने हा आयटम ओळखला आणि तुमच्या पीसीचे संरक्षण करण्यासाठी तो ब्लॉक किंवा लॉग केला.",
        "This does not always mean malware, but security-related settings were modified and should be reviewed.":
            "याचा अर्थ नेहमी मालवेअर नसतो, पण सुरक्षा संबंधित सेटिंग बदलली गेली आहे आणि ती तपासली पाहिजे.",
    },
}

STEP_MAP = {
    "en": {
        "Do not open the file.": "Do not open the file.",
        "Delete the file if you do not trust it.": "Delete the file if you do not trust it.",
        "Run a full system scan.": "Run a full system scan.",
        "Review where the file came from.": "Review where the file came from.",
        "Remove it if you do not need it.": "Remove it if you do not need it.",
        "Run a scan if you are unsure.": "Run a scan if you are unsure.",
        "No action is required.": "No action is required.",
        "Your Defender detection pipeline is working.": "Your Defender detection pipeline is working.",
        "Do not open or run the file again.": "Do not open or run the file again.",
        "Open Windows Security and review Protection history.": "Open Windows Security and review Protection history.",
        "Run a quick or full scan.": "Run a quick or full scan.",
        "Open Windows Security and review recent changes.": "Open Windows Security and review recent changes.",
        "Confirm that real-time protection and other protections are still enabled.": "Confirm that real-time protection and other protections are still enabled.",
        "If the change was unexpected, run a scan.": "If the change was unexpected, run a scan.",
    },
    "hi": {
        "Do not open the file.": "फ़ाइल को न खोलें।",
        "Delete the file if you do not trust it.": "यदि फ़ाइल पर भरोसा नहीं है तो उसे हटा दें।",
        "Run a full system scan.": "पूरा सिस्टम स्कैन चलाएँ।",
        "Review where the file came from.": "फ़ाइल कहाँ से आई है यह जाँचें।",
        "Remove it if you do not need it.": "यदि आवश्यकता न हो तो इसे हटा दें।",
        "Run a scan if you are unsure.": "यदि संदेह हो तो स्कैन चलाएँ।",
        "No action is required.": "कोई कार्रवाई आवश्यक नहीं है।",
        "Your Defender detection pipeline is working.": "आपकी डिफेंडर डिटेक्शन पाइपलाइन सही काम कर रही है।",
        "Do not open or run the file again.": "फ़ाइल को दोबारा न खोलें और न चलाएँ।",
        "Open Windows Security and review Protection history.": "विंडोज सिक्योरिटी खोलें और प्रोटेक्शन हिस्ट्री देखें।",
        "Run a quick or full scan.": "क्विक या फुल स्कैन चलाएँ।",
        "Open Windows Security and review recent changes.": "विंडोज सिक्योरिटी खोलें और हाल के बदलाव देखें।",
        "Confirm that real-time protection and other protections are still enabled.": "पुष्टि करें कि रियल-टाइम प्रोटेक्शन और अन्य सुरक्षा विकल्प चालू हैं।",
        "If the change was unexpected, run a scan.": "यदि बदलाव अप्रत्याशित था तो स्कैन चलाएँ।",
    },
    "mr": {
        "Do not open the file.": "फाइल उघडू नका.",
        "Delete the file if you do not trust it.": "फाइलवर विश्वास नसेल तर ती हटवा.",
        "Run a full system scan.": "पूर्ण सिस्टम स्कॅन चालवा.",
        "Review where the file came from.": "फाइल कुठून आली ते तपासा.",
        "Remove it if you do not need it.": "गरज नसेल तर ती काढून टाका.",
        "Run a scan if you are unsure.": "शंका असल्यास स्कॅन चालवा.",
        "No action is required.": "काही कारवाई आवश्यक नाही.",
        "Your Defender detection pipeline is working.": "तुमची डिफेंडर डिटेक्शन पाइपलाइन व्यवस्थित काम करत आहे.",
        "Do not open or run the file again.": "फाइल पुन्हा उघडू किंवा चालवू नका.",
        "Open Windows Security and review Protection history.": "विंडोज सिक्युरिटी उघडा आणि प्रोटेक्शन हिस्ट्री तपासा.",
        "Run a quick or full scan.": "क्विक किंवा पूर्ण स्कॅन चालवा.",
        "Open Windows Security and review recent changes.": "विंडोज सिक्युरिटी उघडा आणि अलीकडील बदल तपासा.",
        "Confirm that real-time protection and other protections are still enabled.": "रिअल-टाइम प्रोटेक्शन आणि इतर सुरक्षा पर्याय अजूनही सुरू आहेत याची खात्री करा.",
        "If the change was unexpected, run a scan.": "बदल अनपेक्षित असेल तर स्कॅन चालवा.",
    },
}


def localize_title(title: str, lang: str) -> str:
    return TITLE_MAP.get(lang, TITLE_MAP["en"]).get(title, title)


def localize_explanation(text: str, lang: str) -> str:
    return EXPLANATION_MAP.get(lang, EXPLANATION_MAP["en"]).get(text, text)


def localize_step(step: str, lang: str) -> str:
    return STEP_MAP.get(lang, STEP_MAP["en"]).get(step, step)


def build_why_text(alert, lang: str) -> str:
    file_name = os.path.basename(alert.file_path) if alert.file_path else "Unknown File"
    threat = alert.threat_name or "Unknown Threat"

    if lang == "hi":
        return f"थ्रेट {threat} फाइल {file_name} में पाया गया।"
    if lang == "mr":
        return f"धोका {threat} ही फाइल {file_name} मध्ये आढळला."
    return f"Threat {threat} was found in {file_name}."


def render_alert_for_language(alert, lang: str) -> dict:
    return {
        "title": localize_title(alert.title or "", lang),
        "why": build_why_text(alert, lang),
        "explanation": localize_explanation(alert.explanation or "", lang),
        "steps": [localize_step(step, lang) for step in (alert.recommended_steps or [])],
    }


def build_popup_text(alert, lang: str) -> str:
    rendered = render_alert_for_language(alert, lang)
    steps = "\n".join(f"• {step}" for step in rendered["steps"])

    labels = {
        "en": ("TITLE", "THREAT", "FILE/PATH", "WHY BLOCKED", "EXPLANATION", "RECOMMENDED STEPS"),
        "hi": ("शीर्षक", "थ्रेट", "फाइल/पाथ", "क्यों रोका गया", "व्याख्या", "सुझाए गए कदम"),
        "mr": ("शीर्षक", "धोका", "फाइल/पाथ", "का रोखले", "स्पष्टीकरण", "सुचवलेली पावले"),
    }
    l = labels.get(lang, labels["en"])

    return (
        f"{l[0]}: {rendered['title']}\n\n"
        f"{l[1]}: {alert.threat_name or 'Unknown Threat'}\n"
        f"{l[2]}: {alert.file_path or 'Unknown Path'}\n\n"
        f"{l[3]}:\n{rendered['why']}\n\n"
        f"{l[4]}:\n{rendered['explanation']}\n\n"
        f"{l[5]}:\n{steps if steps else '• -'}"
    )


def build_speech_text(alert, lang: str, max_steps: int) -> str:
    rendered = render_alert_for_language(alert, lang)

    prefixes = {
        "en": "Security alert.",
        "hi": "सुरक्षा चेतावनी।",
        "mr": "सुरक्षा इशारा.",
    }

    explain_labels = {
        "en": "Explanation:",
        "hi": "व्याख्या:",
        "mr": "स्पष्टीकरण:",
    }

    steps_labels = {
        "en": "Recommended steps:",
        "hi": "सुझाए गए कदम:",
        "mr": "सुचवलेली पावले:",
    }

    parts = [
        prefixes.get(lang, prefixes["en"]),
        f"{rendered['title']}.",
        f"{rendered['why']}.",
    ]

    if rendered["explanation"]:
        parts.append(f"{explain_labels.get(lang, explain_labels['en'])} {rendered['explanation']}.")

    if rendered["steps"]:
        parts.append(steps_labels.get(lang, steps_labels["en"]))
        parts.append(". ".join(rendered["steps"][:max_steps]) + ".")

    return " ".join(parts)