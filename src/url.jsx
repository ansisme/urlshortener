import React, { useState } from 'react';
import axios from 'axios';

const UrlShortenerForm = () => {
  const [longUrl, setLongUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        'https://0xzsmzj2le.execute-api.us-east-1.amazonaws.com/dev/create', // Replace with your API Gateway URL
        { long_url: longUrl }
      );

      setShortUrl(response.data.result.shortUrl);
    } catch (error) {
      console.error('Error creating short URL:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h1 className='text-align:center'>URL Shortener</h1>
        <label>
          Long URL:
          <input
            type="url"
            value={longUrl}
            onChange={(e) => setLongUrl(e.target.value)}
            required
          />
        </label>
        <button type="submit">Shorten URL</button>
      </form>
      {shortUrl && (
        <div>
          <p>Short URL:</p>
          <a href={longUrl} target="_blank" rel="noopener noreferrer">
            {shortUrl}
          </a>
        </div>
      )}
    </div>
  );
};

export default UrlShortenerForm;
