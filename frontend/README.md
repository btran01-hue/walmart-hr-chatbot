# Walmart HR Chatbot - Frontend

🐶 A modern, accessible React frontend for the Walmart HR Chatbot, built with TypeScript, Tailwind CSS, and WCAG 2.2 Level AA compliance.

## Features

- ✨ Clean, modern chat interface
- ♿ WCAG 2.2 Level AA compliant (keyboard navigation, screen reader support, color contrast)
- 📱 Responsive design (mobile, tablet, desktop)
- ⚡ Fast development with Vite
- 🎨 Walmart brand colors
- 🔗 Microsoft List fallback integration
- 💬 Real-time chat with conversation history
- 🎯 TypeScript for type safety

## Accessibility Features

This application conforms to **WCAG 2.2 Level AA guidelines** including:

- **Keyboard Navigation**: Full keyboard support (Tab, Enter, Shift+Enter)
- **Screen Reader Support**: Proper ARIA labels and roles
- **Color Contrast**: Meets minimum 4.5:1 ratio for text
- **Focus Indicators**: Clear focus outlines (2px blue ring)
- **Semantic HTML**: Proper heading hierarchy and landmarks
- **Form Labels**: All inputs properly labeled
- **Live Regions**: Chat updates announced to screen readers
- **Alternative Text**: Icons have proper aria-labels

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. **Install dependencies:**

```bash
cd frontend
npm install
```

2. **Configure environment (optional):**

```bash
cp .env.example .env
```

For local development, you can leave `.env` empty. The Vite proxy will forward API requests to `localhost:8000`.

For production, set:

```env
VITE_API_URL=https://your-backend-api.com
```

### Running the Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The optimized build will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatContainer.tsx    # Main container with state management
│   │   ├── ChatInput.tsx        # Message input form
│   │   ├── FallbackBanner.tsx   # Microsoft List fallback banner
│   │   ├── Header.tsx           # App header
│   │   ├── Message.tsx          # Individual message component
│   │   └── MessageList.tsx      # Message list with auto-scroll
│   ├── api.ts                   # Backend API client
│   ├── types.ts                 # TypeScript type definitions
│   ├── App.tsx                  # Root component
│   ├── main.tsx                 # Application entry point
│   └── index.css                # Global styles
├── public/                      # Static assets
├── index.html                   # HTML template
├── package.json                 # Dependencies
├── tsconfig.json                # TypeScript config
├── tailwind.config.js           # Tailwind CSS config
├── vite.config.ts               # Vite config
└── README.md                    # This file
```

## Component Architecture

### ChatContainer (Parent)
Manages:
- Chat state (messages, loading, errors)
- API communication
- Fallback logic

### MessageList
- Displays conversation history
- Auto-scrolls to latest message
- Shows loading indicator
- Renders fallback banner

### ChatInput
- Handles user input
- Form submission
- Keyboard shortcuts (Enter/Shift+Enter)

### Message
- Renders individual chat messages
- Different styling for user vs assistant
- Timestamps

### FallbackBanner
- Shown when bot confidence is low
- Links to Microsoft List
- Accessible alert styling

## Customization

### Walmart Branding

Colors are defined in `tailwind.config.js`:

```javascript
colors: {
  'walmart-blue': '#0071ce',
  'walmart-yellow': '#ffc220',
  'walmart-dark': '#041e42',
}
```

### Styling

The app uses Tailwind CSS. Modify component classes or extend the theme in `tailwind.config.js`.

### API Integration

API calls are centralized in `src/api.ts`. Modify the base URL or add authentication headers as needed.

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- Code splitting with Vite
- Tree-shaking for minimal bundle size
- Optimized production builds
- Fast dev server with HMR

## Deployment

### Static Hosting (Recommended)

1. Build the app: `npm run build`
2. Deploy `dist/` folder to:
   - Walmart's internal hosting
   - Azure Static Web Apps
   - Netlify
   - Vercel
   - Any static host

### Environment Variables

Set `VITE_API_URL` to your backend API URL in production.

## Troubleshooting

### API Connection Issues

- Ensure backend is running on `localhost:8000`
- Check CORS settings in backend
- Verify `VITE_API_URL` in `.env`

### Build Errors

- Clear node_modules: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf node_modules/.vite`

## Accessibility Testing

Test with:
- Screen readers (NVDA, JAWS, VoiceOver)
- Keyboard-only navigation
- Browser DevTools accessibility audits
- [axe DevTools](https://www.deque.com/axe/devtools/)

## Contributing

When adding features:
1. Maintain WCAG 2.2 Level AA compliance
2. Keep components under 200 lines
3. Use TypeScript for type safety
4. Test keyboard navigation
5. Test with screen readers

## Support

For issues or questions, contact Walmart Global Tech team.
