import { useState } from 'react';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  const [url, setUrl] = useState<string>('');
  const [audioFormat, setAudioFormat] = useState<string>('mp3');
  const [message, setMessage] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);


  const handleDownload = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/download', {
        url,
        audio_format: audioFormat,
      }, { responseType: 'arraybuffer' });

      const fileExtension = audioFormat === 'mp3' ? 'mp3' : audioFormat === 'flac' ? 'flac' : 'wav';
      const blob = new Blob([response.data], { type: `audio/${fileExtension}` });


      const fileName = response.headers['x-video-title'];

      const urldl = URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.href = urldl;
      a.download = `${fileName}.${fileExtension}`;

      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      setMessage('Download completed successfully.');
    } catch (error: any) {
      setMessage('Error: ' + error.response?.data?.error || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className='w-screen flex flex-col items-center justify-center'>

      <div className='flex'>
        <b className="text-2xl font-semibold mb-4 dark:text-white -tracking-wide">YouTube</b>
        <p className="text-2xl font-light mb-4 dark:text-white -tracking-wide">Downloader</p>
      </div>
      <div className='flex'>
        <input
          type="text"
          placeholder="Enter YouTube video URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="px-4 py-2 border outline-none rounded-l-full dark:bg-[#0e0e0e] dark:border-white placeholder:text-sm"
        />

        <button
          onClick={handleDownload}
          disabled={loading}
          className={`px-4 py-1 flex items-center stroke-black hover:stroke-white bg-[#ffffff] text-black rounded-r-full shadow-md hover:bg-[#000000] hover:text-white focus:outline-none focus:ring-2 focus:bg-[#2e2e2e] ${loading ? 'opacity-100 cursor-not-allowed bg-[#000000]' : ''
            }`}
        >
          {loading ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              className="animate-spin h-6 w-6"
              fill="none"
              stroke="#ffffff"
            >
              <circle cx="12" cy="12" r="10" stroke="#ffffff" strokeWidth="2" />
              <path
                fill="#ffffff"
                d="M12 6v6l4 2"
              />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width={800}
              height={800}
              fill="none"
              viewBox="0 0 24 24"
              className="h-6 w-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 21h12M12 3v14m0 0 5-5m-5 5-5-5"
              />
            </svg>
          )}
        </button>
      </div>
      <br />
      <div className="">
        <label className="dark:text-white">
          <p className=' tracking-widest uppercase text-[11px] font-bold'>Audio Format</p>
          <select
            value={audioFormat}
            onChange={(e) => setAudioFormat(e.target.value)}
            className="px-4 py-3 border-[#1b1b1b] bg-[#0e0e0e] outline-none dark:border-white placeholder:text-sm"
          >
            <option value="mp3">MP3</option>
            <option value="wav">WAV</option>
            <option value="flac">FLAC</option>
          </select>

        </label>
        &nbsp;&nbsp;&nbsp;
      </div>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
      />
      {message && toast(message)}
    </div>
  );
}

export default App;
