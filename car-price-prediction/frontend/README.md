# Frontend (React + TypeScript)

This frontend is the user interface for the CarCast used-car valuation app. It connects to the FastAPI backend and provides prediction, deal analysis, and prediction history in a clean single-page experience.


## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```


## Environment variable

Set backend base URL in [.env](D:/Car-price-prediction-project.worktrees/car-price-prediction-documentation/frontend/.env):

```env
VITE_API_BASE_URL=http://localhost:8000
```