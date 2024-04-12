# Import the SqlServer module
Import-Module SqlServer -Force

# Get the directory where SqlServer module is installed
$modulePath = (Get-Module -Name SqlServer).Path
$assemblyPath = Join-Path -Path $modulePath -ChildPath "Microsoft.SqlServer.Management.IntegrationServices.dll"

# Load the assembly
$loadStatus = [System.Reflection.Assembly]::LoadFrom($assemblyPath)

# Check if assembly loaded successfully
if ($loadStatus) {
    Write-Host "Assembly loaded successfully."
} else {
    Write-Host "Failed to load assembly."
    exit 1  # Exit with an error code if assembly loading fails
}

# Variables
$SSISNamespace = "Microsoft.SqlServer.Management.IntegrationServices"
$TargetServerName = "0.tcp.eu.ngrok.io,12490"
$TargetFolderName = "SSIS-DataFlowAuditing"
$ProjectFilePath = "DatabaseAdministration/SSIS/Ispac/SSIS-DataFlowAuditing.ispac"

$ProjectName = "SSIS-DataFlowAuditing"

# Create a connection to the server
$sqlConnectionString = "Data Source=$TargetServerName;Initial Catalog=master;Integrated Security=SSPI;"
$sqlConnection = New-Object System.Data.SqlClient.SqlConnection $sqlConnectionString

# Create the Integration Services object
$integrationServices = New-Object "$SSISNamespace.IntegrationServices" $sqlConnection

# Get the Integration Services catalog
$catalog = $integrationServices.Catalogs["SSISDB"]

# Create the target folder
$folder = New-Object "$SSISNamespace.CatalogFolder" ($catalog, $TargetFolderName, "Folder description")
$folder.Create()

Write-Host "Deploying $ProjectName project ..."

# Read the project file and deploy it
$projectFile = [System.IO.File]::ReadAllBytes($ProjectFilePath)
$folder.DeployProject($ProjectName, $projectFile)

Write-Host "Done."
