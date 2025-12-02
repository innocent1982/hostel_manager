import { LocationView } from "./components/locationview.js";
import {BrowserRouter as Router, Routes, Route} from "react-router-dom"; 
import {HomePage} from "./pages/home.js";
import {BookPage} from "./pages/book.js";

function App() {
  return (  
  <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/book" element={<BookPage />} /> / 
      </Routes>
  </Router>
  );
}

export default App;
