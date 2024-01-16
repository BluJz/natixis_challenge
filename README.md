# natixis_challenge

# Table of Contents
1. [Introduction](#Introduction)
2. [Installation](#Installation)
3. [Usage](#Usage)
5. [Acknowledgements](#Acknowledgements)

# Introduction

In the context of growing flow activity at Global Markets, secondary bond trading setup has been reshaped (new traders and new sales). To further boost
market-making activity, developing a tool that will help quickly turning traders' positions is critical. Such tool will support sales efforts to reach-out
investors with the highest probability of appetite for our axes. The tool would work 2 ways :
• From an axis seller or buyer of Natixis (ISIN code), recommend a list of clients that should be interested
• From a client name, recommend a list of bonds he could be interested in.

# Installation

### **Prerequisites**
  - This project requires Python 3.9 or higher

### **Steps**

1. **Clone the repository**:

  ```python
  git clone https://github.com/BluJz/natixis_challenge.git
  ```


2. **Navigate to the project directory**:
  ```python
  cd natixis_challenge
  ```


3. **Set up a virtual environment**:
  ```python
  conda create --name natixis_env python=3.9
  conda activate natixis_env
  ```


4. **Install dependencies**:
  ```pyhton
  pip install -r requirements.txt
  ```

5. **Create a database from natixis "RFQ_Data_Challenge_HEC" .csv file**:
 
 After placing "RFQ_Data_Challenge_HEC.csv" in your local repository, run :
  ```pyhton
  python src\\stats_db_creation.py
  ```
Now you're all set !

# Usage
 To run on data :
 ```pyhton
 python src/main.py
 ```

# Dockerize
To Build a Docker image from this repository :
```pyhton
docker build -t natixis_challenge:v0 . -f Dockerfile.app
```

# Acknowledgements
Danli Liu
François Moreau 
Matthieu Haguenauer
Marine Chouraqui