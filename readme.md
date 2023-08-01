# Sniptubez - Simple YouTube Downloader with Python + Vite React TypeScript

Sniptubez is a simple YouTube downloader built using Python for the backend and Vite with React and TypeScript for the frontend. It allows users to download YouTube videos for offline viewing.

## Project Structure

```
📦 sniptubez
├─ .gitignore
├─ app.py
├─ frontend
│  ├─ .eslintrc.cjs
│  ├─ .gitignore
│  ├─ README.md
│  ├─ index.html
│  ├─ package.json
│  ├─ postcss.config.js
│  ├─ public
│  │  └─ vite.svg
│  ├─ src
│  │  ├─ App.css
│  │  ├─ App.tsx
│  │  ├─ assets
│  │  │  └─ react.svg
│  │  ├─ index.css
│  │  ├─ main.tsx
│  │  └─ vite-env.d.ts
│  ├─ tailwind.config.js
│  ├─ tsconfig.json
│  ├─ tsconfig.node.json
│  ├─ vite.config.ts
│  └─ yarn.lock
├─ requirements.txt
└─ test
   └─ rootdir.py
```

## Backend

The backend of the project is implemented using Python. The main entry point is `app.py`, which will handle the server and the API endpoints to process YouTube video download requests.

## Frontend

The frontend is built using Vite, React, and TypeScript. The main source code for the frontend is located in the `frontend/src` directory. The entry point for the frontend is `frontend/src/main.tsx`. The UI components and logic are defined in various files inside the `src` directory.

## Dependencies and Configuration Files

The project includes various configuration files such as `.eslintrc.cjs`, `postcss.config.js`, `tailwind.config.js`, `tsconfig.json`, `tsconfig.node.json`, and `vite.config.ts` for setting up the development environment and build processes.

## Installation and Setup

To run the project, you'll need to install the required Python packages listed in `requirements.txt`. Additionally, you'll need Node.js and yarn for setting up the frontend. To install the frontend dependencies, navigate to the `frontend` directory and run `yarn install`.

## Usage

To start the development server for the frontend, navigate to the `frontend` directory and run `yarn dev`. For the backend, run the `app.py` file.

## Note

Please ensure that you use this project responsibly and adhere to the YouTube terms of service when downloading videos. The project is provided for educational purposes only.