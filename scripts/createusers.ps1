param (
    [string]$username,
    [string]$password,
    [string]$firstname,
    [string]$lastname
)

$securePassword = ConvertTo-SecureString -String $password -AsPlainText -Force
$UserInfo = @{
    Name = $username
    Password = $securePassword
    FullName = "$firstname $lastname"
    Description = "Created via automated script"
    PasswordNeverExpires = $false
    UserMayNotChangePassword = $false
}
try {
    $user = New-LocalUser @UserInfo
    Write-Output "User created: $($user.Name)"
} catch {
    Write-Error "Failed to create user: $_"
}
