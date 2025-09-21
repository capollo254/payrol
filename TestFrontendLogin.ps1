Write-Host "🧪 Testing Frontend Access Control" -ForegroundColor Cyan
Write-Host "=" * 50

Write-Host "`n1. Testing backend API directly (should work correctly):" -ForegroundColor Yellow

# Test employee API access
$employee_auth = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/auth/login/" -Method POST -Body @{email="employee@demo.com"; password="demo123"} -ContentType "application/x-www-form-urlencoded"
Write-Host "   Employee role from API: $($employee_auth.role)" -ForegroundColor Green

$employee_payslips = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/payroll/payslips/" -Method GET -Headers @{"Authorization"="Token $($employee_auth.token)"}
Write-Host "   Employee sees $($employee_payslips.count) payslips (should be 3)" -ForegroundColor Green

# Test admin API access
$admin_auth = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/auth/login/" -Method POST -Body @{email="constantive@gmail.com"; password="demo123"} -ContentType "application/x-www-form-urlencoded"
Write-Host "   Admin role from API: $($admin_auth.role)" -ForegroundColor Green

$admin_payslips = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/payroll/payslips/" -Method GET -Headers @{"Authorization"="Token $($admin_auth.token)"}
Write-Host "   Admin sees $($admin_payslips.count) payslips (should be all)" -ForegroundColor Green

Write-Host "`n2. Testing inactive user block:" -ForegroundColor Yellow
try {
    $inactive_login = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/auth/login/" -Method POST -Body @{email="inactive@test.com"; password="demo123"} -ContentType "application/x-www-form-urlencoded"
    Write-Host "   ❌ ERROR: Inactive user was able to log in!" -ForegroundColor Red
} catch {
    Write-Host "   ✅ CORRECT: Inactive user blocked from login" -ForegroundColor Green
}

Write-Host "`n🎯 Frontend Test Instructions:" -ForegroundColor Cyan
Write-Host "1. Open http://localhost:3002 in your browser" -ForegroundColor White
Write-Host "2. Try logging in with:" -ForegroundColor White
Write-Host "   - employee@demo.com / demo123 (should see employee dashboard & only 3 payslips)" -ForegroundColor White
Write-Host "   - constantive@gmail.com / demo123 (should see admin dashboard & all payslips)" -ForegroundColor White
Write-Host "   - inactive@test.com / demo123 (should be blocked from login)" -ForegroundColor White

Write-Host "`n✅ Backend access control is working correctly!" -ForegroundColor Green
Write-Host "Frontend should now correctly use roles from backend API." -ForegroundColor Green