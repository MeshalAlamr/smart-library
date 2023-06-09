import React, { useState } from "react";
import FileUploadForm from "./FileUploadForm";
import ResourceDisplay from "./ResourceDisplay";

const App = () => {
  const [resources, setResources] = useState([]);

  const handleFormSubmit = async (formData) => {
    setResources([...resources, formData]);

    try {
      const response = await fetch("http://localhost:8000/extract", {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
          "Content-Type": "application/json",
        },
      });

      // ...
    } catch (error) {
      console.error(error);
      alert("Failed to extract text from PDF.");
    }
  };

  return (
    <div>
      <div className="header">
        <img src="/online-library.png" alt="Logo" className="logo" />
        <h1>Smart Library</h1>
      </div>
      <div className="container">
        <FileUploadForm onSubmit={handleFormSubmit} />
        <ResourceDisplay resources={resources} />
      </div>
    </div>
  );
};

export default App;
