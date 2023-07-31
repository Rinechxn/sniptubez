import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';

const DarkModeToggle: React.FC = () => {
  const [darkMode, setDarkMode] = useState<boolean>(false);

  useEffect(() => {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setDarkMode(prefersDark);

    const handleDarkModeChange = (e: MediaQueryListEvent) => {
      setDarkMode(e.matches);
    };

    const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    darkModeMediaQuery.addEventListener('change', handleDarkModeChange);

    return () => {
      darkModeMediaQuery.removeEventListener('change', handleDarkModeChange);
    };
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
  }, [darkMode]);

  return (
    <button
      className="fixed right-5 bottom-5 p-3 rounded-full bg-gray-500 dark:bg-gray-900 text-white"
      onClick={() => setDarkMode((prev) => !prev)}
    >
      {darkMode ? '🌞' : '🌙'}
    </button>
  );
};

ReactDOM.render(
  <React.StrictMode>
    <App />
    <DarkModeToggle />
  </React.StrictMode>,
  document.getElementById('root')
);
