# Frontend

## Getting Started

- First, install Node.js and Node Package Manager (npm) (yarn works as well).
- Second, run ```npm install``` to install dependencies.
    - Use ```cd frontend/``` to move into the root of the frontend folder.
- Finally, use either of the following commands to run the local development server [deployed on [http://localhost:3000](http://localhost:3000)]:

```bash
npm run dev
# or
pnpm run dev
```

## How It Works

This frontend is built with [Next.js](https://nextjs.org/) and [React](https://react.dev/). It uses a component-based architecture for modularity and maintainability. The main features include:

- **Dynamic Routing:** Pages are organized in the `/app` directory, following Next.js conventions.
- **Reusable Components:** UI elements such as the navbar, footer, and custom features are located in `/app/ui-components`.
- **State Management:** React hooks (`useState`, `useEffect`, etc.) are used for local component state.
- **API Integration:** Data fetching is handled using Next.js server functions or React hooks.

## Project Structure

```
frontend/
├── app/
│   ├── ui-components/    # Reusable React components
│   ├── layout.tsx        # Layout for the entire application
│   ├── page.tsx          # Main entry page
│   └── ...
├── public/               # Static assets (images, icons, etc.)
├── README.md
├── package.json
└── ... Other dependencies ...
```

## Styling

- **CSS Modules:** Local component styles are defined in `.module.css` files.
- **Tailwind CSS:** Utility-first CSS framework for rapid UI development (if enabled in your project).
- **Custom Animations:** Keyframes and gradients are used for interactive and animated UI elements.

## How to Contribute

1. Clone this repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "Add your message"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a pull request.


