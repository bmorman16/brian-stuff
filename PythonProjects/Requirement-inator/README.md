# t4_requirements_helper



## Getting started
Get Administrative Access through upep https://upep.web.boeing.com

Once access has been granted run granular control in Software Express 

Run the DevOps Setup Script in powershell and ensure the following utilities are selected for install and hit "Install Packages"

Visit this page if you're running into issue on this step: https://git.web.boeing.com/DevHub/devops-setup/

![powershell.png](images/powershell.png)

```
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; iex ((New-Object Net.WebClient).DownloadString('https://git.web.boeing.com/DevHub/devops-setup/-/raw/master/components/devops-setup/devops-setup.ps1')); exit
```
![devops_setup.PNG](images/devops_setup.PNG)
## Setting Up The Environment
Open  Powershell 7

![powershell 7.png](images/powershell 7.png)

Clone the Repository
```
git clone https://git.web.boeing.com/daniel.s.ellerbrock/t4_requirements_helper.git
```
Open the Repository
```
cd ./t4_requirements_helper
```

Run The Setup script
```
./setup.ps1
```

## Running the Script 
Edit the Path to where your review excel sheet is
![excel_path.PNG](images/excel_path.PNG)

Open  Powershell 7

![powershell 7.png](images/powershell 7.png)

Ensure you are in the right repository for example
```
cd ./t4_requirements_helper
```

Run the run script

```
./run.ps1
```

