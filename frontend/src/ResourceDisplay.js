import React from "react";

const ResourceDisplay = ({ resources }) => {
  return (
    <div className="container">
      <div className="resource-display">
        <h2>Uploaded Resources</h2>
        {resources.map((resource, index) => (
          <div className="resource-card" key={index}>
            <p>Resource Type: {resource.resourceType}</p>
            <p>Resource Name: {resource.resourceName}</p>
            <p>Publish Year: {resource.publishYear}</p>
            <p>Author: {resource.author}</p>
            <p>File: {resource.file.name}</p>
            <p>PDF Text: {resource.pdfText}</p>{" "}
            {/* Display the extracted PDF text */}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResourceDisplay;
