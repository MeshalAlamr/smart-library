import React, { useState } from "react";

const FileUploadForm = ({ onSubmit }) => {
  const [resourceType, setResourceType] = useState("");
  const [resourceName, setResourceName] = useState("");
  const [publishYear, setPublishYear] = useState("");
  const [author, setAuthor] = useState("");
  const [pdfText, setPdfText] = useState("");

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    const fileType = file.type;
    const allowedFileType = "application/pdf";

    if (fileType !== allowedFileType) {
      alert("Please upload a PDF file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/extract", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to extract text from PDF.");
      }

      const data = await response.json();

      // Access the extracted text from the response
      const pdfText = data.data;

      // Call the onSubmit function with the extracted text and form data
      onSubmit({ resourceType, resourceName, publishYear, author, pdfText });

      // Reset the form fields
      setResourceType("");
      setResourceName("");
      setPublishYear("");
      setAuthor("");
      setPdfText("");
    } catch (error) {
      console.error(error);
      alert("Failed to extract text from PDF.");
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const formData = {
      resourceType,
      resourceName,
      publishYear,
      author,
    };
    onSubmit(formData);
    setResourceType("");
    setResourceName("");
    setPublishYear("");
    setAuthor("");
  };

  return (
    <div className="container">
      <h1>Smart Library</h1>
      <div className="file-upload-form">
        <h2>Upload a Resource</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Resource Type:
            <input
              type="text"
              value={resourceType}
              onChange={(e) => setResourceType(e.target.value)}
            />
          </label>
          <label>
            Resource Name:
            <input
              type="text"
              value={resourceName}
              onChange={(e) => setResourceName(e.target.value)}
            />
          </label>
          <label>
            Publish Year:
            <input
              type="text"
              value={publishYear}
              onChange={(e) => setPublishYear(e.target.value)}
            />
          </label>
          <label>
            Author:
            <input
              type="text"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
            />
          </label>
          <label>
            File Upload:
            <input type="file" onChange={handleFileUpload} />
          </label>
          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
};

export default FileUploadForm;
