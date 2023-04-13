# MPDW Project

#### Project members:

- Rodrigo Ralha Moreira <rr.moreira@campus.fct.unl.pt>(mailto:rr.moreira@campus.fct.unl.pt)
- João Nuno Santos <jnc.santos@campus.fct.unl.pt>(mailto:jnc.santos@campus.fct.unl.pt)
- Louis CHATARD <l.chatard@campus.fct.unl.pt>(mailto:l.chatard@campus.fct.unl.pt)

#### Project supervisor

João Miguel da Costa Magalhães

## Project description

This project is made in the context of the course "Web Search and Data Mining" of the Master in Computer Science at the Nova FCT University.
The aim is to create a chatbot extension that can be used on the [Farfetch](farfetch.com) website to search items and eventually get recommandations based on the user's preferences.
It's based on the already existing extension [iFetch](https://github.com/pmvalente171/iFetch-Chrome-Extension)

## Project Setup

The Project Setup uses the config.py file which contains information like the credentials to access OpenSearch Service. However, due to security issues, this credentials are being hide. In order to being able to use it, you have to setup your environment variables in one of the following alternatives:

### WINDOWS

#### Method 1: Set Environment Variables Temporarily for the Current Session

1. Open the Command Prompt or PowerShell.
2. Set the environment variables using the set command (replace your_username and your_password with the actual values):
   2a. set OPENSEARCH_USER=ifetch
   2b. set OPENSEARCH_PASSWORD=S48YdnMQ

These environment variables will only be available for the current session. When you close the Command Prompt or PowerShell, the variables will be lost.

#### Method 2: Set Environment Variables Permanently

1. Press Win + X and click on "System" in the menu that appears.
2. Click on "Advanced system settings" on the right side.
3. In the "System Properties" window that appears, click on the "Environment Variables" button near the bottom.
4. In the "Environment Variables" window, under "User variables" or "System variables" (depending on whether you want the variables to be available for just the current user or for all users), click on the "New" button.
5. Enter the variable name (OPENSEARCH_USER) and value (ifetch) in the "Variable name" and "Variable value" fields, respectively, and click "OK".
6. Repeat steps 4 and 5 to add another environment variable for OPENSEARCH_PASSWORD.
7. Click "OK" to close the "Environment Variables" window, and then click "OK" again to close the "System Properties" window.

### LINUX

#### Method 1

1. nano ~/.bashrc
2. Scroll to the end of the file and add the following lines (replace your_username and your_password with the actual values):
   2a. export OPENSEARCH_USER=ifetch
   2b. export OPENSEARCH_PASSWORD=S48YdnMQ
3. after saving run: source ~/.bashrc
