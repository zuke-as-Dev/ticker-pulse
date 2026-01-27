import hashlib

def story_hash(title: str) -> str:
    key = title.lower().strip()
    return hashlib.sha1(key.encode()).hexdigest()
