# Start the timer
$startTime = Get-Date
$timestamp = $startTime.ToString("yyyyMMdd_HHmmss")

# Initialize counters
$successCount = 0
$failureCount = 0
$iteration = 1
$failedTests = @()

# Create log paths
$sessionLogPath = "logs/test_session_$timestamp.log"
$failureDir = "logs/failures"
New-Item -ItemType Directory -Force -Path $failureDir | Out-Null

try {
  while ($true) {
    # Run tests and capture output
    $result = python -m pytest tests/ -m "not manual" --disable-warnings --tb=short -s 2>&1

    # General session log
    Add-Content -Path $sessionLogPath -Value "===== ITERATION #$iteration ====="
    Add-Content -Path $sessionLogPath -Value $result
    Add-Content -Path $sessionLogPath -Value "`n"

    if ($result -match "FAILED") {
      Write-Host "Test #$iteration failed." -ForegroundColor Red
      $failureCount++
      $failedTests += $iteration

      # Per-test failure log
      $failureLogFile = "$failureDir/test_fail_iter_$iteration.log"
      Add-Content -Path $failureLogFile -Value "===== FAILURE TEST #$iteration ====="
      Add-Content -Path $failureLogFile -Value $result
      Add-Content -Path $failureLogFile -Value "`n"
    }
    else {
      Write-Host "Test #$iteration passed." -ForegroundColor Green
      $successCount++
    }

    $iteration++
  }
}
finally {
  # End the timer
  $endTime = Get-Date
  $elapsed = $endTime - $startTime
  $totalTests = $successCount + $failureCount
  $passRate = "{0:P2}" -f ($successCount / $totalTests)

  # Test summary
  Write-Host "`n========= TEST SUMMARY =========" -ForegroundColor Cyan
  Write-Host "Total tests   : $totalTests"     -ForegroundColor Cyan
  Write-Host "Passed        : $successCount"   -ForegroundColor Green
  Write-Host "Failed        : $failureCount"   -ForegroundColor Red
  Write-Host "Success rate  : $passRate"       -ForegroundColor Yellow

  if ($failedTests.Count -gt 0) {
    Write-Host "`nFailed Test Iterations:" -ForegroundColor Red
    $failedTests | ForEach-Object { Write-Host " - Iteration #$_" -ForegroundColor Red }
  }

  Write-Host "`nTotal execution time: $($elapsed.ToString("hh\:mm\:ss\.fff"))" -ForegroundColor Cyan
}
