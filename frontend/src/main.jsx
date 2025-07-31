import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// Debug: log when dark mode class changes
const observer = new MutationObserver(() => {
  const html = document.documentElement;
  console.log('HTML classList:', html.classList.value);
});
observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
)
