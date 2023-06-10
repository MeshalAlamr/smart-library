
# Smart Library

## Demo

### Team 1 Task (Librarians)
**Description:**<br>
- The user uploads a PDF file and fills in the information.
- The file is sent to the backend server to be processed.
- The backend server using tysseract and HuggingFace models does the following:
  - Extracts the text from the PDF file.
  - Summarizes the text.
  - Predicts the topics of the text.
  - Predicts the sentiment of the text.
- The results are sent back to the user and displayed on the screen. 
- The user can then edit the information if needed. After that, the user can confirm and the information will be added to the MongoDB database.


![Team1](https://github.com/MeshalAlamr/smart-library/assets/68873733/756aeaf3-bafa-43c4-8c9f-a2fc72993d4e)

### Team 2 Task (Users)
**Description:**<br>
- The user enters a query in the search bar.
- The query is sent to the backend server to be processed.
- The backend server using HuggingFace models does the following:
  - Embeds the summaries of the books in the database.
  - Embeds the query. 
  - Finds the most similar summary to the query.
  - Returns the related document.
- The results are sent back to the user and displayed on the screen.
- Additionally, if an OpenAI API key is provided, the query, summary, topic, and sentiment are sent to the OpenAI API to generate a response as a helpful librarian. The response is then displayed on the screen.

![Team2](https://github.com/MeshalAlamr/smart-library/assets/68873733/a1076c72-dc70-4bc4-9bbe-2601475e256c)

## Getting Started

Clone the repository

```
git clone https://github.com/MeshalAlamr/smart-library.git
```

Move to project directory

```
cd smart-library
```


### Note:
If you want to use the Librarian's Answer feature, you need to provide your OpenAI API key in the .env file. You can get one from [here](https://beta.openai.com/).

Modify the .env file to include your API key

```
OPENAI_API_KEY='Your Key Here'
```

 This project supports both running on Docker or locally.
<br>

### Using Docker:
<details>
<summary>Docker</summary>
<br>
  
```shell
docker compose up
```
  
</details>


### Installing locally:
<details>
<summary>Local</summary>
<br>
Start by creating a Conda environmnet or whichever environment manager you prefer.
<br><br>
Install requirements

```shell
pip install -r requirements.txt
```


### **Backend Server**
1. From the project directory, navigate to the backend directory
   ```shell
   cd services
   ```

2. Download the models
   ```
   python download_models.py
   ```

3. Start the backend server
   ```
   python app.py
   ```

### **Web Server**
> **Note:** The backend server must be running before starting the web server.
1. Start another terminal, from the project directory, navigate to the server directory
   ```shell
   cd server
   ```

2. Start the server
   ```
   python run.py
   ```

</details>

### After running the server, open the browser and go to http://127.0.0.1:3000/ to start.
