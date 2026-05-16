# policies/safety_policies.py
# Rule layer for ACSIF. These are intentionally explicit and inspectable.

POLICIES = {
    "HIGH": {
        "action": "BLOCK",
        "description": (
            "Block unsafe content, avoid harmful details, and redirect the child "
            "to a trusted adult."
        ),
    },
    "MEDIUM": {
        "action": "MODIFY",
        "description": (
            "Allow only after softening, correcting unsafe assumptions, and giving "
            "safe educational guidance."
        ),
    },
    "LOW": {
        "action": "ALLOW",
        "description": "Allow normal age-adaptive response generation.",
    },
}


BLOCKED_RESPONSE_BY_AGE = {
    "6-8": (
        "I cannot help with that because it may not be safe. "
        "Please talk to a parent, teacher, or another trusted adult."
    ),
    "9-12": (
        "I cannot help with that request because it may involve safety or privacy risks. "
        "Please speak with a trusted adult before doing anything."
    ),
    "13-15": (
        "I cannot provide help with that because it could be unsafe or involve privacy risk. "
        "Please involve a trusted adult or responsible authority."
    ),
}
