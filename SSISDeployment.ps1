# Import the SqlServer module
Import-Module SqlServer -Force

# Variables
$SSISNamespace = "Microsoft.SqlServer.Management.IntegrationServices"
$TargetServerName = "0.tcp.eu.ngrok.io,12490"
$TargetFolderName = "SSIS-DataFlowAuditing"
$ProjectFilePath = "DatabaseAdministration/SSIS/Ispac/SSIS-DataFlowAuditing.ispac"
$ProjectName = "SSIS-DataFlowAuditing"

# Load the IntegrationServices assembly
$assemblyPath = "DLL/Microsoft.SqlServer.Management.IntegrationServices"
$loadStatus = [System.Reflection.Assembly]::LoadFrom($assemblyPath)


if ($loadStatus) {
    Write-Host "Assembly loaded successfully."
} else {
    Write-Host "Failed to load assembly."
    exit 1  # Exit with an error code if assembly loading fails
}

# Create a connection to the server
$sqlConnectionString = "Data Source=$TargetServerName;Initial Catalog=master;Integrated Security=SSPI;"
$sqlConnection = New-Object System.Data.SqlClient.SqlConnection $sqlConnectionString

# Create the Integration Services object
$integrationServices = New-Object "$SSISNamespace.IntegrationServices" $sqlConnection

if ($integrationServices -eq $null) {
    Write-Host "Failed to create Integration Services object."
    exit 1  # Exit with an error code if object creation fails
}

# Get the Integration Services catalog
$catalog = $integrationServices.Catalogs["SSISDB"]

if ($catalog -eq $null) {
    Write-Host "Failed to get SSISDB catalog."
    exit 1  # Exit with an error code if catalog retrieval fails
}

# Create the target folder
$folder = New-Object "$SSISNamespace.CatalogFolder" ($catalog, $TargetFolderName, "Folder description")
$folder.Create()

Write-Host "Deploying $ProjectName project ..."

# Read the project file and deploy it
$projectFile = [System.IO.File]::ReadAllBytes($ProjectFilePath)
$folder.DeployProject($ProjectName, $projectFile)

Write-Host "Done."
