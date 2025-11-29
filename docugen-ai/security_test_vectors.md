# Security Test Vectors for Repository URL Validation

## 1. Command Injection
- `https://github.com/user/repo; rm -rf /`
- `https://github.com/user/repo && echo 'pwned'`
- `https://github.com/user/repo | cat /etc/passwd`
- `--upload-pack=touch /tmp/pwned`
- `-oProxyCommand=calc`

## 2. Server-Side Request Forgery (SSRF)
- `http://localhost:8080/git`
- `http://127.0.0.1:22/user/repo`
- `http://169.254.169.254/latest/meta-data/` (AWS Metadata)
- `http://0.0.0.0:8000/`
- `http://[::1]:80/`
- `http://internal-service.local/repo.git`

## 3. Protocol Attacks
- `file:///etc/passwd`
- `ftp://example.com/repo.git`
- `gopher://example.com/1`
- `dict://example.com/d:word`

## 4. Path Traversal
- `https://github.com/../../etc/passwd`
- `https://github.com/user/repo/../../../`
- `/etc/passwd` (Absolute path)
- `../../../../tmp`

## 5. Invalid Characters & Format
- `https://github.com/user/repo%00` (Null byte)
- `https://github.com/user/repo\n` (Newline)
- `javascript:alert(1)`
- `data:text/plain;base64,SGVsbG8=`

## 6. Credential Leaks (Should be blocked)
- `https://user:password@github.com/org/repo.git`
- `https://token@github.com/org/repo.git`
