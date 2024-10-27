# Define variables
$requirementsFile = ".\requirements.txt"
$testExcludedRequirementsFile = ".\test-excluded-requirements.txt"
$outputFile = ".\test-requirements.txt"
$encoding = "utf8"

# Get the content of test-excluded-requirements.txt
$testExcludedRequirements = Get-Content -Path $testExcludedRequirementsFile

# Find lines in requirements.txt that do not match any line in test-excluded-requirements.txt
$testRequirements = Select-String -Path $requirementsFile -NotMatch $testExcludedRequirements | ForEach-Object { $_.Line }

# Output the excluded lines to the specified file with utf8 encoding
$testRequirements | Out-File -FilePath $outputFile -Encoding $encoding
