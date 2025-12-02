import "bootstrap/dist/css/bootstrap.min.css";
import "./css/output.css";

function App() {
  return (
    <div className="text-bg-light flex flex-col gap-1 min-h-[90vh]">
      <nav class="navbar bg-body-tertiary">
        <div class="container-fluid">
          <a class="fs-1 h1 navbar-brand text-xl font-extrabold" href="#">
            Angonia
          </a>
          <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
        </div>
      </nav>
      <div className="container flex flex-col items-center">
        <h1 className="text-3xl pt-10 font-extrabold max-w-[70vw]">
          The Cheapest and closest to campus hostel at NRC
        </h1>
        <div className="pt-3 [&>*]: [&>*]:text-md ">
          <p>View and book rooms easily</p>
          <p>Make payments seemlessly</p>
          <p>Track hostel analytics easily</p>
        </div>
        <button className="btn btn-light shadow-md mt-3 bg-gray-300 rounded-md">
          Book Now
        </button>
        <button className="btn btn-secondary mt-3 shadow-md rounded-md ">
          View Rooms
        </button>
      </div>
      <div className="mt-20 flex flex-col gap-1">
        <div>
          <p className="pt-5 text-center font-bold text-xl mx-auto ">
            Locations
          </p>
        </div>
        <div
          id="carouselExampleIndicators"
          className="carousel slide max-w-[90%] mx-auto rounded-md shadow-md"
        >
          <div class="carousel-indicators">
            <button
              type="button"
              data-bs-target="#carouselExampleIndicators"
              data-bs-slide-to="0"
              class="active"
              aria-current="true"
              aria-label="Slide 1"
            ></button>
            <button
              type="button"
              data-bs-target="#carouselExampleIndicators"
              data-bs-slide-to="1"
              aria-label="Slide 2"
            ></button>
            <button
              type="button"
              data-bs-target="#carouselExampleIndicators"
              data-bs-slide-to="2"
              aria-label="Slide 3"
            ></button>
          </div>
          <div className="rounded-md carousel-inner">
            <div class="carousel-item active">
              <img src="/a.jpg" class="d-block w-100" alt="..." />
            </div>
            <div class="carousel-item">
              <img src="/b.jpg" class="d-block w-100" alt="..." />
            </div>
            <div class="carousel-item">
              <img src="/c.jpg" class="d-block w-100" alt="..." />
            </div>
          </div>
          <button
            class="carousel-control-prev"
            type="button"
            data-bs-target="#carouselExampleIndicators"
            data-bs-slide="prev"
          >
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
          </button>
          <button
            class="carousel-control-next"
            type="button"
            data-bs-target="#carouselExampleIndicators"
            data-bs-slide="next"
          >
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
