param (
    [string] $ReportPath = "DatabaseAdministration/SSRS/Reports/DepReportNew.rdl",
    [string] $ReportServerUri = "http://desktop-6jdns4n/ReportServer",
    [string] $TargetFolder = "/SharedReports"
)

# Error handling: stop script on error
$ErrorActionPreference = "Stop"

# Import ReportingServicesTools module
Import-Module -Name ReportingServicesTools

# Check if ReportPath is provided
if (-not (Test-Path $ReportPath -PathType Leaf)) {
    Write-Error "Report file not found at '$ReportPath'."
    exit 1
}

# Check if ReportServerUri ends with a slash
if (-not $ReportServerUri.EndsWith("/")) {
    $ReportServerUri += "/"
}

# Check if TargetFolder starts with a slash
if (-not $TargetFolder.StartsWith("/")) {
    $TargetFolder = "/" + $TargetFolder
}

# Get report file name
$ReportName = (Get-Item $ReportPath).Name

# Specify target report path
$TargetReportPath = $TargetFolder + "/" + $ReportName

# Deploy report to target folder
Write-Output "Deploying report '$ReportName' to folder '$TargetFolder' on report server '$ReportServerUri'..."
try {
    Write-RsCatalogItem -ReportServerUri $ReportServerUri -Path $ReportPath -Destination $TargetFolder -Verbose -Overwrite
    Write-Output "Report deployed successfully."
} catch {
    Write-Error "Failed to deploy report: $_"
    exit 1
}
