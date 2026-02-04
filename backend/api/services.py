"""
Password analysis services
"""
import hashlib
import re
import requests


def calculate_password_strength(password: str) -> dict:
    """
    Calculate password strength with detailed criteria
    Returns score (0-100), strength label, feedback, and criteria breakdown
    """
    criteria = {
        'length': len(password) >= 8,
        'length_12': len(password) >= 12,
        'length_16': len(password) >= 16,
        'uppercase': bool(re.search(r'[A-Z]', password)),
        'lowercase': bool(re.search(r'[a-z]', password)),
        'numbers': bool(re.search(r'\d', password)),
        'special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
        'no_common': not is_common_password(password),
        'no_sequential': not has_sequential_chars(password),
        'no_repeated': not has_repeated_chars(password),
    }
    
    # Calculate score
    score = 0
    
    # Length scoring (up to 30 points)
    if criteria['length']:
        score += 10
    if criteria['length_12']:
        score += 10
    if criteria['length_16']:
        score += 10
    
    # Character variety (up to 40 points)
    if criteria['uppercase']:
        score += 10
    if criteria['lowercase']:
        score += 10
    if criteria['numbers']:
        score += 10
    if criteria['special']:
        score += 10
    
    # Security patterns (up to 30 points)
    if criteria['no_common']:
        score += 10
    if criteria['no_sequential']:
        score += 10
    if criteria['no_repeated']:
        score += 10
    
    # Determine strength label
    if score >= 90:
        strength = 'very_strong'
    elif score >= 70:
        strength = 'strong'
    elif score >= 50:
        strength = 'good'
    elif score >= 30:
        strength = 'fair'
    else:
        strength = 'weak'
    
    # Generate feedback
    feedback = []
    if not criteria['length']:
        feedback.append('Use pelo menos 8 caracteres')
    elif not criteria['length_12']:
        feedback.append('Considere usar 12+ caracteres para maior segurança')
    
    if not criteria['uppercase']:
        feedback.append('Adicione letras maiúsculas')
    if not criteria['lowercase']:
        feedback.append('Adicione letras minúsculas')
    if not criteria['numbers']:
        feedback.append('Adicione números')
    if not criteria['special']:
        feedback.append('Adicione caracteres especiais (!@#$%)')
    if not criteria['no_common']:
        feedback.append('Evite senhas comuns')
    if not criteria['no_sequential']:
        feedback.append('Evite sequências (123, abc)')
    if not criteria['no_repeated']:
        feedback.append('Evite caracteres repetidos (aaa, 111)')
    
    if not feedback:
        feedback.append('Excelente! Senha muito forte 💪')
    
    return {
        'score': score,
        'strength': strength,
        'feedback': feedback,
        'criteria': criteria,
    }


def is_common_password(password: str) -> bool:
    """Check if password is in common passwords list"""
    common = [
        'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey', 
        'master', 'dragon', 'admin', 'letmein', 'login', 'welcome',
        'password1', 'p@ssw0rd', 'iloveyou', 'princess', 'sunshine',
        'passw0rd', '654321', 'superman', 'qwerty123', '1234567890',
    ]
    return password.lower() in common


def has_sequential_chars(password: str) -> bool:
    """Check for sequential characters like 123 or abc"""
    sequences = [
        '012', '123', '234', '345', '456', '567', '678', '789', '890',
        'abc', 'bcd', 'cde', 'def', 'efg', 'fgh', 'ghi', 'hij', 'ijk',
        'jkl', 'klm', 'lmn', 'mno', 'nop', 'opq', 'pqr', 'qrs', 'rst',
        'stu', 'tuv', 'uvw', 'vwx', 'wxy', 'xyz',
        'qwe', 'wer', 'ert', 'rty', 'tyu', 'yui', 'uio', 'iop',
        'asd', 'sdf', 'dfg', 'fgh', 'ghj', 'hjk', 'jkl',
        'zxc', 'xcv', 'cvb', 'vbn', 'bnm',
    ]
    lower = password.lower()
    return any(seq in lower for seq in sequences)


def has_repeated_chars(password: str) -> bool:
    """Check for 3+ repeated characters"""
    return bool(re.search(r'(.)\1{2,}', password))


def check_hibp_breach(password: str) -> tuple[bool, int]:
    """
    Check if password appears in Have I Been Pwned database
    Uses k-anonymity: only sends first 5 chars of SHA1 hash
    
    Returns: (is_breached, breach_count)
    """
    # SHA1 hash the password
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    try:
        # Query HIBP API with prefix only (k-anonymity)
        response = requests.get(
            f'https://api.pwnedpasswords.com/range/{prefix}',
            headers={'User-Agent': 'SecurePass-Dashboard'},
            timeout=5
        )
        
        if response.status_code != 200:
            return False, 0
        
        # Search for our suffix in the response
        hashes = response.text.splitlines()
        for line in hashes:
            hash_suffix, count = line.split(':')
            if hash_suffix == suffix:
                return True, int(count)
        
        return False, 0
        
    except requests.RequestException:
        # If API fails, return unknown (not breached)
        return False, 0


def get_hash_prefix(password: str) -> str:
    """Get the first 5 characters of SHA1 hash (for k-anonymity storage)"""
    return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()[:5]
