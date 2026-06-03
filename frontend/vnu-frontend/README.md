# VNU Frontend

Frontend application built with React + TypeScript + Vite.

## Development Server

To start a local development server, run:

```bash
npm install
npm run dev
```

Once the server is running, open your browser and navigate to `http://localhost:5173/`. The application will automatically reload whenever you modify any of the source files.

## Runtime Config (Local vs Deploy)

- **Local Development**: `npm run dev` reads configuration from `public/assets/app-config.js` (pointing to `http://localhost:8081`)
- **Deploy**: Container frontend generates `public/assets/app-config.js` from environment variables `APP_API_BASE_URL` and `APP_GOOGLE_CLIENT_ID` (no manual code changes needed)

## Building

To build the project for production, run:

```bash
npm run build
```

This will compile your project and store the build artifacts in the `dist/` directory. The production build optimizes your application for performance and speed.

## Running Tests

To execute unit tests, use:

```bash
npm test
```

## Code Generation

To generate a new component, run:

```bash
npm run generate component component-name
```

## ESLint

To check and fix code style issues:

```bash
npm run lint
npm run lint:fix
```

## Additional Resources

For more information on Vite, visit the [Vite Documentation](https://vite.dev/).
For React documentation, see [React Docs](https://react.dev/).
