/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "../../frontend/templates/**/*.html",
      "../../frontend/static/src/**/*.js",
      "../../frontend/node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      fontFamily: {
        IBMPlex: ["IBMPlex"],
      },
    },
    
  },
  plugins: [
    require("flowbite/plugin")
  ],
}