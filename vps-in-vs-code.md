Method 1: Connecting via Remote-SSH (Recommended)
This is the standard way to use your local VS Code application to manage a remote Hostinger VPS. 

Get SSH Credentials: Log in to your Hostinger hPanel, navigate to VPS → Manage, and find your IP Address and Username (usually root) under the SSH access tab.
Install the Extension: In VS Code, go to the Extensions view (Ctrl+Shift+X), search for Remote - SSH by Microsoft, and click Install.
Add Your VPS:
Press F1 or Ctrl+Shift+P and type Remote-SSH: Add New SSH Host....
Enter the connection command: ssh root@your_vps_ip.
Select the configuration file to save it in (usually the first option: ~/.ssh/config).
Connect:
Click the Remote Explorer icon in the sidebar (it looks like a small monitor).
Right-click your VPS IP under "SSH" and select Connect to Host in Current Window.
If prompted, select the platform (e.g., Linux) and enter your VPS password.
Open Folders: Once connected (a green badge in the bottom-left corner will show your IP), go to File > Open Folder to browse and edit your server's files directly.

ssh key path:-
C:\Users\Admin\.ssh
