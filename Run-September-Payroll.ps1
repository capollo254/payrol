# PowerShell Script to Run September 2025 Payroll
# This script handles authentication and API calls properly

Write-Host "🚀 Starting September 2025 Payroll Run" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Yellow

# Step 1: Test server connectivity
try {
    Write-Host "🔍 Testing server connectivity..." -ForegroundColor Cyan
    $testResponse = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/auth/" -Method GET -ErrorAction Stop
    Write-Host "✅ Server is responsive" -ForegroundColor Green
} catch {
    Write-Host "❌ Server is not running. Please start Django server first:" -ForegroundColor Red
    Write-Host "   cd backend" -ForegroundColor Yellow
    Write-Host "   python manage.py runserver" -ForegroundColor Yellow
    exit 1
}

# Step 2: Authenticate and get token
try {
    Write-Host "🔐 Authenticating..." -ForegroundColor Cyan
    
    $authBody = @{
        email = "employee@demo.com"
        password = "demo123"
    }
    
    $authResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/auth/login/" -Method POST -Body $authBody -ContentType "application/x-www-form-urlencoded" -ErrorAction Stop
    
    $token = $authResponse.token
    Write-Host "✅ Authentication successful" -ForegroundColor Green
    Write-Host "   Token: $($token.Substring(0, 20))..." -ForegroundColor Gray
    
} catch {
    Write-Host "❌ Authentication failed" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Step 3: Create payroll run
try {
    Write-Host "💼 Creating September 2025 payroll run..." -ForegroundColor Cyan
    
    $headers = @{
        "Authorization" = "Token $token"
        "Content-Type" = "application/json"
    }
    
    $payrollBody = @{
        period_start_date = "2025-09-01"
        period_end_date = "2025-09-30"
    } | ConvertTo-Json
    
    $payrollResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/payroll/payroll-runs/" -Method POST -Headers $headers -Body $payrollBody -ErrorAction Stop
    
    Write-Host "✅ Payroll run created successfully!" -ForegroundColor Green
    Write-Host "   📋 Payroll Run ID: $($payrollResponse.id)" -ForegroundColor White
    Write-Host "   📅 Run Date: $($payrollResponse.run_date)" -ForegroundColor White
    Write-Host "   📊 Period: $($payrollResponse.period_start_date) to $($payrollResponse.period_end_date)" -ForegroundColor White
    Write-Host "   👤 Run By User ID: $($payrollResponse.run_by)" -ForegroundColor White
    
} catch {
    Write-Host "❌ Payroll creation failed" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    
    # Try to get more detailed error information
    if ($_.Exception.Response) {
        $errorStream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($errorStream)
        $errorBody = $reader.ReadToEnd()
        Write-Host "   Response: $errorBody" -ForegroundColor Red
    }
    exit 1
}

# Step 4: Check generated payslips
try {
    Write-Host "📄 Checking generated payslips..." -ForegroundColor Cyan
    
    $payslipsResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/payroll/payslips/" -Method GET -Headers $headers -ErrorAction Stop
    
    $payslipCount = $payslipsResponse.count
    Write-Host "✅ Payslips generated: $payslipCount" -ForegroundColor Green
    
    if ($payslipCount -gt 0) {
        Write-Host "📋 Recent payslips:" -ForegroundColor White
        $payslipsResponse.results | Select-Object -First 5 | ForEach-Object {
            $employeeName = $_.employee.full_name
            $netPay = $_.net_pay
            Write-Host "   • $employeeName : KES $netPay" -ForegroundColor White
        }
    }
    
} catch {
    Write-Host "⚠️  Could not fetch payslips, but payroll run was created" -ForegroundColor Yellow
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 September 2025 Payroll Process Completed!" -ForegroundColor Green
Write-Host "You can view detailed payslips in the frontend at http://localhost:3001" -ForegroundColor Cyan