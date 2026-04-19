param (
    [Parameter(Mandatory=$true)]
    [string]$SourceFile,
    
    [int]$Processes = 4
)

# Extract the filename without the .cpp extension to name the executable
$basename = [System.IO.Path]::GetFileNameWithoutExtension($SourceFile)
$exeName = "$basename.exe"

# Hardcoded paths to bypass PowerShell string parsing issues
$inc = "C:\Program Files (x86)\Microsoft SDKs\MPI\Include"
$lib = "C:\Program Files (x86)\Microsoft SDKs\MPI\Lib\x64"

Write-Host "--> Compiling C++ file $SourceFile..." -ForegroundColor Cyan
# Using g++ instead of gcc for C++ compilation
g++ -o $exeName $SourceFile -I"$inc" -L"$lib" -lmsmpi

# Check if compilation was successful before trying to run
if ($LASTEXITCODE -eq 0) {
    Write-Host "--> Build successful! Executing with $Processes processes...`n" -ForegroundColor Green
    mpiexec -n $Processes .\$exeName
} else {
    Write-Host "--> Compilation failed. Check your C++ code for errors." -ForegroundColor Red
}