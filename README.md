
# Smart Library

![Logo](./assets/book.png)

You are tasked to create to improve the public library of your local community by allow people to interact with books, articles, newspapers and magazines in the library with the help of Artificial Intelligentce. There are two teams assigned to complete two related sub-tasks for this project to enable library users to digital interact with the content:

1. Team 1: Create an interface that librarians could use to upload books, articles, newspapers and magazines as PDF and and a Machine Learning Model will extract the text, summarize and classify it and save it to a database. 
2. Team 2: Create an interface for library users to write a query and an AI model will compare it to all the summaries of books and return the best result. 

</br>

![Portrait](./assets/library.jpg)

## Tech Stack

### Operating System
Linux kernel 5.15.0-72-generic Ubuntu Linux Desktop 20.04 Focal Fossa

### Dependencies 
- Tesseract OCR: Follow the installation instruction 
  ```shell
  https://github.com/tesseract-ocr/tesseract
  ```
  
### Services

1. **backend**: Huggingface, Pytorch, Tensorflow, pytesseract, FastAPI
2. **frontend**: React
4. **database**: mongoDB

## Installation

### **backend**
1. Install python 3.10.0
   > You can choose any python environment management system you prefer (conda, pyenv, venv ... etc)
2. Navigate to the ai directory
   ```shell
   cd ai
   ```
3. Install the python packages
   ```shell
   pip install -r requirements.txt
   ```
4. Navigate to the src directory 
    ```shell
    cd src
    ```
5. Run the FastAPI server
   ```shell
   python server.py
   ```

### **backend**
### **database**
### **frontend**

## Instructions

Your goal is to choose which team you want play and depedning on the team complete the following tasks for each section. A skeleton is provided as a starter code.</br>

You will be following a microservice architecture to help the library summarize, classify and retrieve relevent entries based on queries library users write. After successfuly complete the application. You will write the necessary Docker and Docker Compose files to deploy the application (Well, only locally for now 💻). 


#### Team 1
1. Create simple page with a file upload form along with text boxes to write the details of the resource (e.g. resource type: [book, article, newspaper, magaznine], resource name, publish year, author ... etc)
   > A sample data is provided under database directory
2. Use Huggingface models to summaries the resource 
   > A function is already provided to extract text from pdf files
   
   > Bonus: Use a Question-Answering model or text classification model
3. Write an endpoint to save the summary along with the resource details to database

#### Team 2
1. Create a simple page with query text box for library users to enter any search point.
2. Use Huggingface model to get the most relevant resource from the database text similarity from the resource summary
3. Write an endpoint to get the query from text box, go through the resource enteries, get similarities and return the most releveant resource name


## Deployment
Create Dockerfiles for each services and a Docker Compose file for a multi-service deployment. 
  
## Authors
- [@mort8Q](https://www.github.com/mort8q)

  
  

## Submission
1. Please clone your copy of this repository:
```shell
git clone https://github.com/mort8q/ml-task
```
2. Complete the tasks mentioned under [Instructions](#instructions) for for the team you have chosen.
3. You are encourged to git, commit your changes at multiple stages of your work. 
4. Compress your project folder with (zip, tar, or 7z) formats
6. Email back your work within 72 hours

