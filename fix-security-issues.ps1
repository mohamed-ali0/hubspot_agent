# Fix Security Issues Script
# Removes hardcoded API keys and commits the changes

Write-Host "🔒 Fixing Security Issues" -ForegroundColor Red
Write-Host "=========================" -ForegroundColor Red

# Check if git is available
try {
    git --version | Out-Null
    Write-Host "✅ Git is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not available. Please install Git first." -ForegroundColor Red
    exit 1
}

Write-Host "`n🔍 Checking for hardcoded API keys..." -ForegroundColor Yellow

# Check if hardcoded tokens still exist
$hardcodedTokens = @(
    "pat-eu1-df4fa9c7-df17-4174-a492-37f6091b2e21",
    "pat-na1-",
    "pat-eu1-",
    "pat-ap1-"
)

$foundTokens = @()
foreach ($token in $hardcodedTokens) {
    $result = git grep -n $token 2>$null
    if ($result) {
        $foundTokens += $result
    }
}

if ($foundTokens.Count -gt 0) {
    Write-Host "❌ Found hardcoded tokens:" -ForegroundColor Red
    $foundTokens | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
    Write-Host "`nPlease remove these hardcoded tokens before pushing." -ForegroundColor Red
    exit 1
} else {
    Write-Host "✅ No hardcoded tokens found" -ForegroundColor Green
}

Write-Host "`n📝 Adding security fixes..." -ForegroundColor Yellow

# Add the fixed files
git add setup_test_user_with_token.py
git add test_hubspot_fix.py

Write-Host "✅ Added security fixes" -ForegroundColor Green

Write-Host "`n💾 Committing security fixes..." -ForegroundColor Yellow

# Commit the security fixes
git commit -m "security: Remove hardcoded HubSpot API keys

- Remove hardcoded API tokens from test files
- Use environment variables instead of hardcoded values
- Add proper error handling for missing tokens
- Fix GitHub secret scanning violations"

Write-Host "✅ Security fixes committed" -ForegroundColor Green

Write-Host "`n🚀 Pushing to repository..." -ForegroundColor Yellow

# Push to repository
git push origin master

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Successfully pushed to repository!" -ForegroundColor Green
    Write-Host "`n🎉 Security issues resolved!" -ForegroundColor Green
    Write-Host "Your HubSpot AI Agent is now ready for deployment!" -ForegroundColor Cyan
} else {
    Write-Host "❌ Push failed. Check the error messages above." -ForegroundColor Red
    Write-Host "You may need to resolve additional security issues." -ForegroundColor Red
}
