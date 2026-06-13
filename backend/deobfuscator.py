import re
import base64

class PHPDeobfuscator:
    def __init__(self):
        pass

    def remove_comments(self, code):
        """Removes junk comments that attackers use to break up code signatures."""
        # Remove multi-line comments /* ... */
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        # Remove single-line comments // ...
        code = re.sub(r'//.*', '', code)
        return code

    def resolve_concatenation(self, code):
        """Fixes split strings. Converts 'e'.'v'.'a'.'l' back to 'eval'."""
        # Target common PHP concatenation patterns
        code = re.sub(r"' \. '", "", code)
        code = re.sub(r'" \. "', "", code)
        code = re.sub(r"'\.'", "", code)
        code = re.sub(r'"\."', "", code)
        return code

    def decode_hex(self, code):
        """Converts hex byte codes (\x65) back to ASCII characters (e)."""
        def hex_repl(match):
            try:
                return chr(int(match.group(1), 16))
            except ValueError:
                return match.group(0)
        return re.sub(r'\\x([0-9a-fA-F]{2})', hex_repl, code)

    def decode_base64_payloads(self, code):
        """Finds base64_decode('...') and replaces it with the actual hidden code."""
        # Regex to find base64_decode() functions containing valid base64 strings
        pattern = r"base64_decode\(\s*['\"]([A-Za-z0-9+/=]+)['\"]\s*\)"
        
        def b64_repl(match):
            try:
                # Decode it, ignoring errors if the base64 is malformed
                decoded = base64.b64decode(match.group(1)).decode('utf-8', errors='ignore')
                return decoded
            except Exception:
                return match.group(0)
                
        # Run it a few times in a loop to catch nested decodes: base64_decode(base64_decode(...))
        for _ in range(3):
            code = re.sub(pattern, b64_repl, code)
        return code

    def clean(self, raw_code):
        """The main pipeline that runs all cleaning steps."""
        if not isinstance(raw_code, str):
            return ""
            
        code = self.remove_comments(raw_code)
        code = self.resolve_concatenation(code)
        code = self.decode_hex(code)
        code = self.decode_base64_payloads(code)
        
        # Strip out excess whitespace to make it dense and readable for the AI
        code = re.sub(r'\s+', ' ', code).strip()
        return code

# --- Quick Test ---
if __name__ == "__main__":
    sample_malware = """
    <?php 
    /* junk comment to hide from antivirus */
    $func = 'b'.'a'.'s'.'e'.'6'.'4'.'_'.'d'.'e'.'c'.'o'.'d'.'e'; 
    eval($func('c3lzdGVtKCJ3aG9hbWkiKTs=')); 
    ?>
    """
    
    cleaner = PHPDeobfuscator()
    print("--- RAW MALWARE ---")
    print(sample_malware.strip())
    print("\n--- DEOBFUSCATED OUTPUT ---")
    print(cleaner.clean(sample_malware))